# -*- coding: utf-8 -*-
import json
import logging
import sys
import requests
from eaglet.decorator import param_required
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business import model as business_model
from business.mall.wzcard import WZCard
from db.mall import models as mall_models
from db.mall import promotion_models

from util import regional_util
from business.mall.order import Order
from business.mall.supplier import Supplier
from business.account.user_profile import UserProfile
# from business.mall.express.express_service import ExpressService
# from business.market_tools.template_message.order_template_message_service import OrderTemplageMessageService

from business.account.integral import Integral
from business.member.webapp_user import WebAppUser
from business.member.member_spread import MemberSpread

from services.order_notify_mail_service.task import service_send_order_email
from services.shiped_order_template_message_service.task import service_send_shiped_order_template_message
from services.express_service.task import service_express
import settings

FATHER_ORDER = 1
CHILD_ORDER = 2
SELF_ORDER = 0

class OrderState(Order):
    """
    OrderState对象 只涉及状态
    """

    def __init__(self, model):
        Order.__init__(self, model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        order_db_model = mall_models.Order.select().dj_where(id=args['id'])
        if order_db_model.count() == 0:
            return None
        order = OrderState(order_db_model.first())
        return order

    @staticmethod
    @param_required(['order_id'])
    def from_order_id(args):
        order_db_model = mall_models.Order.select().dj_where(order_id=args['order_id']).first()
        if not order_db_model:
            return None
        order = OrderState(order_db_model)
        return order
    @staticmethod
    @param_required(['order_ids'])
    def from_order_ids(args):
        order_db_models = mall_models.Order.select().dj_where(order_id__in=args['order_ids'])
        orders = []
        for model in order_db_models:
            orders.append(OrderState(model))
        return orders

    @staticmethod
    @param_required(['origin_id'])
    def from_origin_id(args):
        order_db_models = mall_models.Order.select().dj_where(origin_order_id=args['origin_id'])
        orders = []
        for order_model in order_db_models:
            order = OrderState(order_model)
            orders.append(order)
        return orders

    def record_status_log(self, operator_name, from_status, to_status):
        try:
            mall_models.OrderStatusLog.create(
                order_id = self.order_id,
                from_status = from_status,
                to_status = to_status,
                operator = operator_name
            )
        except:
            error_msg = u"增加订单({})状态更改记录失败, cause:\n{}".format(order_id, unicode_full_stack())
            watchdog.error(error_msg)


    def record_operation_log(self, operator_name, action, type=SELF_ORDER):
        """
            记录操作日志，未来数据量增大使用异步（celery）方式
        """
        order_id = self.order_id
        if type == FATHER_ORDER:
            if self.origin_order_id > 0:
                origin_order = Order.from_id({
                    "id":self.origin_order_id
                    })
                #处理操作日志
                if self.supplier > 0:  #weapp add by duhao 如果是子订单，则加入供应商信息
                    supplier = Supplier.from_id({
                        "id":self.supplier
                        })
                    action = '%s - %s' % (action, supplier.name)
                if self.supplier_user_id > 0:
                    user_profile = UserProfile.from_webapp_id({
                        "webapp_id": self.webapp_id
                        })
                    action = '%s - %s' % (action, user_profile.store_name)
                order_id = origin_order.order_id

        elif type == CHILD_ORDER:
            if mall_models.Order.select().dj_where(origin_order_id=self.id).count() == 1:
                child_order = Order.from_origin_id({
                    "origin_id":self.id
                    })[0]
                order_id = child_order.order_id

        mall_models.OrderOperationLog.create(order_id=order_id, action=action, operator=operator_name)

    def __send_ship_template_message(self):

        service_send_shiped_order_template_message.delay(self.order_id, self.webapp_id)
        # order_template_message_service = OrderTemplageMessageService.from_webapp_id({
        #     "webapp_id": self.webapp_id,
        #     "send_point": template_message_models.PAY_DELIVER_NOTIFY
        #     })
        # if order_template_message_service:
        #     order_template_message_service.send_order_templage_message(self.order_id)

    def __send_order_email(self, status=None):
        if not status:
            status = self.status
        #使用celery
        service_send_order_email.delay(self.order_id, self.webapp_id, status)


    def __send_request_to_kuaidi(self):
        """
        向快递服务商发送订阅请求
        """
        #TODO  修改参数指定具体参数 不直接传递order对象
        service_express.delay(self.order_id)
        #is_success = ExpressService(self).get_express_poll()



    def update_ship(self, express_company_name,express_number, operator_name=u'我', leader_name=u'', is_100 = True):
        order = self
        target_status = mall_models.ORDER_STATUS_PAYED_SHIPED
        order_params = dict()
        express_number = express_number.replace(' ','')  #快递100服务器过滤空格,快递鸟不过滤空格
        order_params['express_company_name'] = express_company_name
        order_params['express_number'] = express_number
        order_params['leader_name'] = leader_name
        order_params['status'] = target_status
        order_params['is_100'] = is_100
        #order = Order.objects.get(id=order_id)
        self.express_company_name = express_company_name
        self.express_number = express_number

        mall_models.Order.update(**order_params).dj_where(id=self.id).execute()

        action = u'修改发货信息'

        if order.origin_order_id > 0:
            #当前订单为子订单，并且只有一个子订单，则同步更新父订单
            if mall_models.Order.select().dj_where(origin_order_id=order.origin_order_id).count() == 1:
                origin_order = OrderState.from_id({
                    "id": order.origin_order_id
                    })

                Order.update(**order_params).dj_where(id=order.origin_order_id).execute()
                origin_order.record_operation_log(operator_name, action, OrderState.FATHER_ORDER)
        else:
            #当前订单为父订单，并且只有一个子订单，则同步更新子订单
            #TODO order对象增加获取子订单数量函数
            if mall_models.Order.select().dj_where(origin_order_id=order.id).count() == 1:
                child_order = OrderState.from_origin_id({
                    "origin_id": order.id
                    })[0]
                #TODOOrderState增加修改update方法
                mall_models.Order.update(**order_params).dj_where(origin_order_id=order.id).execute()
                 #处理操作日志
                child_order.record_operation_log(operator_name, action,CHILD_ORDER)

        """
            TODO加入到celery tasks:
                1.快递接口访问（快递100或者是快递鸟接口访问）
                2.发送邮件
        """
        self.__send_ship_template_message()
        if is_100:
            self.__send_request_to_kuaidi()

        self.__send_order_email(target_status)

        return True, ''


    def ship(self, express_company_name,express_number, operator_name=u'我', leader_name=u'', is_100 = True):
        #ship_order(order_id, express_company_name,express_number, operator_name=u'我', leader_name=u'', is_update_express=False, is_100 = True):
        """
        进行订单的发货处理：
            express_company_name：快递公司名称
            express_number: 货运单号
            leader_name: 负责人

        处理操作流程：
        1. 修改订单的状态为“已发货”
        2. 修改订单记录，添加运单号和快递公司信息
        3. 增加订单操作记录信息
        4. 增加状态更改记录信息

        如果对应订单不存在，或者操作失败直接返回False
        整个操作过程中如果其中有一个步骤失败则继续之后的操作
        但是会进行预警处理，以便人工进行相应操作

        如果订单id、快递公司名称或运单号任一为None，直接返回False

        如果订单id、快递公司名称或运单号任一长度为0返回False
        """
        #子订单
        if self.origin_order_id == -1:
            child_orders = OrderState.from_origin_id({
                "origin_id":self.id
            })
            if len(child_orders) > 1:
                return False, u'不能对当前订单发货'

        if self.status == mall_models.ORDER_STATUS_PAYED_SHIPED:
            return False, u'订单状态已经改变'

        target_status = mall_models.ORDER_STATUS_PAYED_SHIPED
        order_params = dict()
        express_number = express_number.replace(' ','')  #快递100服务器过滤空格,快递鸟不过滤空格
        order_params['express_company_name'] = express_company_name
        order_params['express_number'] = express_number
        order_params['leader_name'] = leader_name
        order_params['status'] = target_status
        order_params['is_100'] = is_100
        #order = Order.objects.get(id=order_id)
        action = u'订单发货'
        mall_models.Order.update(**order_params).dj_where(id=self.id).execute()
        self.record_status_log(operator_name, self.status, target_status)
        self.record_operation_log(operator_name, action)

        #处理子订单和包含子订单的主订单
        if self.origin_order_id > 0:
            child_orders = Order.from_origin_id({
                "origin_id": self.origin_order_id
                })
            origin_order = OrderState.from_id({
                "id": self.origin_order_id
            })

            children_order_status = [order.status for order in child_orders]

            if origin_order.status != min(children_order_status):
                #所有子订单全部发货更新父订单
                if min(children_order_status) == target_status: #and len(children_order_status) > 1:
                    mall_models.Order.update(status=target_status).dj_where(id=origin_order.id).execute()
                    #mall_models.Order.update(**order_params).dj_where(id=origin_order.id).execute()
                    origin_order.record_status_log(operator_name, origin_order.status, target_status)
                    origin_order.record_operation_log(operator_name, action, FATHER_ORDER)
        elif self.origin_order_id == -1:
            child_order = child_orders[0]
            mall_models.Order.update(**order_params).dj_where(id=child_order.id).execute()
            child_order.record_status_log(operator_name, child_order.status, target_status)
            child_order.record_operation_log(operator_name, action, CHILD_ORDER)


        """
            TODO加入到celery tasks:
                1.快递接口访问（快递100或者是快递鸟接口访问）
                2.发送邮件
        """
        self.__send_ship_template_message()
        if is_100:
            self.__send_request_to_kuaidi()

        self.__send_order_email()

        return True, ''


    def cancel(self, operator_name=u'系统'):
        """
        目前只支持团购业务中的取消订单
        @param operator_name:
        @return:
        """

        # todo
        assert not self.is_sub_order

        target_status = mall_models.ORDER_STATUS_CANCEL
        action = '取消订单'

        # 检查操作

        # 返回优惠券

        # 返回微众卡
        if self.weizoom_card_money:
            self.__return_wzcard()

        # 记录操作日志、更改状态

        # 当前为主订单
        self.record_status_log(operator_name, self.status, target_status)
        self.record_operation_log(operator_name, action, CHILD_ORDER)
        mall_models.Order.update(status=target_status).dj_where(id=self.id).execute()
        print 'cancel', self.child_order_count
        if self.child_order_count > 0:
            child_orders = OrderState.from_origin_id({
                "origin_id": self.origin_order_id
            })
            for child_order in child_orders:
                child_order.record_status_log(operator_name, child_order.status, target_status)
                child_order.record_operation_log(operator_name, action, CHILD_ORDER)

        # 返回商品库存、销量

        self.__restore_product()


        # 返回订单积分

        # 处理首单标记

        # 处理子订单、母订单

        self.__send_order_email()
        return u"订单%s取消成功！" % self.order_id

    def refunding(self, operator_name=u'系统'):
        """
        申请订单退款
        """
        target_status = mall_models.ORDER_STATUS_REFUNDING
        action = '退款中'

        self.record_status_log(operator_name, self.status, target_status)
        self.record_operation_log(operator_name, action, CHILD_ORDER)
        mall_models.Order.update(status=target_status).dj_where(id=self.id).execute()
        print 'refunding', self.child_order_count
        if self.child_order_count > 0:
            child_orders = OrderState.from_origin_id({
                "origin_id": self.origin_order_id
            })
            for child_order in child_orders:
                child_order.record_status_log(operator_name, child_order.status, target_status)
                child_order.record_operation_log(operator_name, action, CHILD_ORDER)

        return u"订单%s正在退款！" % self.order_id

    def refund(self, operator_name=u'系统'):
        """
        目前只支持团购业务中的退款完成订单
        @param operator_name:
        @return:
        """
        assert not self.is_sub_order
        target_status = mall_models.ORDER_STATUS_REFUNDED
        action = '退款完成'

        # 记录操作日志、更改状态

        # 当前为主订单
        self.record_status_log(operator_name, self.status, target_status)
        self.record_operation_log(operator_name, action, CHILD_ORDER)
        mall_models.Order.update(status=target_status).dj_where(id=self.id).execute()
        print 'refund', self.child_order_count
        if self.child_order_count > 0:
            child_orders = OrderState.from_origin_id({
                "origin_id": self.origin_order_id
            })
            for child_order in child_orders:
                child_order.record_status_log(operator_name, child_order.status, target_status)
                child_order.record_operation_log(operator_name, action, CHILD_ORDER)

        # 返回商品库存、销量
        self.__restore_product()

        # 返回微众卡
        if self.weizoom_card_money:
            self.__return_wzcard()
        return u"订单%s退款完成！" % self.order_id

    def return_money(self):
        KEY = 'MjExOWYwMzM5M2E4NmYwNWU4ZjI5OTI1YWFmM2RiMTg='
        if settings.MODE in ['develop', 'test']:
            URL = 'http://pay.weapp.com/refund/weixin/api/order/refund/'
        else:
            URL = 'http://pay/refund/weixin/api/order/refund/'

        args = {
            'order_id': self.order_id,
            'auth_key': KEY,
            'from_where': 'weapp'
        }
        response = dict()
        try:
            logging.info("url:%s" % URL)
            logging.info("args:%s" % str(args))
            r = requests.get(URL, params=args)
            response = json.loads(r.text)
            if not response['data'].get('is_success', ''):
                r = requests.get(URL, params=args)
                response = json.loads(r.text)
                if not response['data'].get('is_success', ''):
                    r = requests.get(URL, params=args)
                    response = json.loads(r.text)
        except:
            try:
                r = requests.get(URL, params=args)
                response = json.loads(r.text)
                if not response['data'].get('is_success', ''):
                    r = requests.get(URL, params=args)
                    response = json.loads(r.text)
            except:
                try:
                    r = requests.get(URL, params=args)
                    response = json.loads(r.text)
                except:
                    logging.info(u"订单退款异常,\n{}".format(unicode_full_stack()))
                    watchdog.alert(u"订单退款异常,\n{}".format(unicode_full_stack()))
                    return u"订单%s通知退退款异常" % self.order_id
        if response['data'].get('is_success', ''):
            self.refund()
            mall_models.Order.update(
                status=mall_models.ORDER_STATUS_GROUP_REFUNDING
                ).dj_where(id=self.id).execute()
            return u"订单%s通知退款成功" % self.order_id
        else:
            logging.info(u"订单%s通知退款失败" % self.order_id)
            watchdog.alert(u"订单%s通知退款失败" % self.order_id)
            return u"订单%s通知退款失败" % self.order_id

    def finish(self, operator_name):
        target_status = mall_models.ORDER_STATUS_SUCCESSED

        if self.status == target_status:
            return False, "order finished"

        if self.status != mall_models.ORDER_STATUS_PAYED_SHIPED:
            return False, "can not finish order not in shiped"

        if self.origin_order_id == -1:
            child_order_count = self.child_order_count
            if child_order_count > 1:
                return False, "can not finish order "
        else:
            child_order_count = 0


        action = '完成'

        # if operation_name:
        #     operation_name = u'{} {}'.format(operation_name, (actions[1] if len(actions) > 1 else ''))
        # else:
        #     operation_name = actions[1] if len(actions) > 1 else ''

        mall_models.Order.update(status=target_status).dj_where(id=self.id).execute()
        self.record_status_log(operator_name, self.status, target_status)
        self.record_operation_log(operator_name, action)

        #更新红包引入消费金额的数据 by Eugene
        if self.coupon_id and promotion_models.RedEnvelopeParticipences.select().dj_where(coupon_id=self.coupon_id, introduced_by__gt=0).count() > 0:
            red_envelope2member = promotion_models.RedEnvelopeParticipences.get(coupon_id=self.coupon_id)
            relation = promotion_models.RedEnvelopeParticipences.update(promotion_models.RedEnvelopeParticipences.introduce_sales_number + self.final_price + self.postage).dj_where(
                red_envelope_rule_id=red_envelope2member.red_envelope_rule_id,
                red_envelope_relation_id=red_envelope2member.red_envelope_relation_id,
                member_id=red_envelope2member.introduced_by
            ).execute()

        origin_order_id = 0

        if self.origin_order_id > 0:
            #所有子订单
            child_orders = Order.from_origin_id({
                "origin_id": self.origin_order_id
                })

            #主订单
            origin_order = OrderState.from_id({
                "id": self.origin_order_id
            })

            children_order_status = [order.status for order in child_orders]

            if origin_order.status != min(children_order_status):
                #所有子订单全部发货更新父订单
                if min(children_order_status) == target_status: #and len(children_order_status) > 1:
                    mall_models.Order.update(status=target_status).dj_where(id=origin_order.id).execute()

                    origin_order.record_status_log(operator_name, origin_order.status, target_status)
                    origin_order.record_operation_log(operator_name, action, FATHER_ORDER)

                    origin_order_id = origin_order.id

        else:
            #当前为主订单
            if child_order_count > 0:
                child_orders = OrderState.from_origin_id({
                    "origin_id": self.origin_order_id
                    })
                mall_models.Order.update(status=target_status).dj_where(origin_order_id=self.id).execute()
                for child_order in child_orders:
                    child_order.record_status_log(operator_name, child_order.status, target_status)
                    child_order.record_operation_log(operator_name, action, CHILD_ORDER)
            origin_order_id = self.id

        if origin_order_id:
            webapp_user = WebAppUser.from_id({
                "id": self.webapp_user_id
                })
            webapp_user.update_pay_info(float(self.final_price) + float(self.weizoom_card_money), self.payment_time)
            MemberSpread.process_order_from_spread({
                'order_id': origin_order_id,
                'webapp_user': webapp_user
                })

            # 订单完成后会员积分处理
            Integral.increase_after_order_payed_finsh({
                'webapp_user': webapp_user,
                'order_id': origin_order_id
            })

        self.__send_order_email()
        return True, ''

    def updat_status(self, status):
        mall_models.Order.update(
            status=status
        ).dj_where(id=self.id).execute()

    def __return_wzcard(self):
        WZCard.refund_for_order(self)

    def __restore_product(self):
        products = self.products

        for product in products:
            models = mall_models.ProductModel.select().dj_where(product_id=product['id'],
                                                             name=product['product_model_name'])
            # 该商品有此规格，并且库存是有限，进入修改商品的数量
            if models.count() > 0 and models[0].stock_type == mall_models.PRODUCT_STOCK_TYPE_LIMIT:
                product_model = models[0]
                product_model.stocks = product_model.stocks + product['count']
                product_model.save()
            # product sales update
            if self.status < mall_models.ORDER_STATUS_PAYED_SUCCESSED or (
                        product.get('promotion', None) and product['promotion'].get('type', '').find(
                        'premium_product') > 0):
                # 订单未支付或者是赠品商品, 不需要回退销量数据
                continue
            productsales = mall_models.ProductSales.select().dj_where(product_id=product.get('id'))

            if productsales:
                try:
                    mall_models.ProductSales.update(sales=mall_models.ProductSales.sales - product['count']).dj_where(
                        product_id=product.get('id')).execute()
                except BaseException as e:
                    watchdog.alert({
                        'uuid': 'return_stock_and_sales_in_zeus',
                        'traceback': unicode_full_stack(),
                        'product_id':product.get('id')
                    })
