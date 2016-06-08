# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business import model as business_model
from db.mall import models as mall_models
from util import regional_util
from business.mall.order import Order
from business.mall.supplier import Supplier
from business.account.user_profile import UserProfile

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
    @param_required(['order_id'])
    def from_order_id(args):
        order_db_model = mall_models.Order.select().dj_where(order_id=args['order_id'])
        if order_db_model.count() == 0:
            return None
        order = OrderState(order_db_model.first())
        #order.ship_area = regional_util.get_str_value_by_string_ids(order_db_model.area)
        return order

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
        if type == OrderState.FATHER_ORDER:
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
            
        elif type == OrderState.CHILD_ORDER:
            if Order.select().dj_where(origin_order_id=self.id).count() == 1:
                child_order = Order.from_origin_id({
                    "origin_order_id":self.id
                    })
                order_id = child_order.order_id

        mall_models.OrderOperationLog.create(order_id=order_id, action=action, operator=operator_name)

    def update_express(self, express_company_name,express_number, operator_name=u'我', leader_name=u'', is_100 = True):
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
        mall_models.Order.update(**order_params).dj_where(id=self.id).execute()
        #TODO
        # try:
        #     if express_company_name and express_number:
        #         order.express_company_name = express_company_name
        #         order.express_number = express_number
        #         order.leader_name = leader_name
        #         #TODO 发货模版消息
        #         #template_message_api.send_order_template_message(order.webapp_id, order.id, template_message_model.PAY_DELIVER_NOTIFY)
        # except:
        #     alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
        #     watchdog.error(alert_message)
        
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
            if mall_models.Order.select().dj_where(origin_order_id=order.id).count() == 1:
                child_order = OrderState.from_origin_id({
                    "origin_id": order.id
                    })

                mall_models.Order.update(**order_params).dj_where(origin_order_id=order.id).execute()
                 #处理操作日志
                child_order.record_operation_log(operator_name, action,OrderState.CHILD_ORDER)
        return True, ''


    def ship_order(self, express_company_name,express_number, operator_name=u'我', leader_name=u'', is_100 = True):
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
                "origin_order_id":self.id
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
            mall_models.Order.update(status=target_status).dj_where(id=child_order.id).execute()
            child_order.record_status_log(operator_name, child_order.status, target_status)
            child_order.record_operation_log(operator_name, action, CHILD_ORDER)

        
        # TODO 发货模版消息
        # try:
        #     if express_company_name and express_number:
        #         order.express_company_name = express_company_name
        #         order.express_number = express_number
        #         order.leader_name = leader_name
                
        #         template_message_api.send_order_template_message(order.webapp_id, order.id, template_message_model.PAY_DELIVER_NOTIFY)
        # except:
        #     alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
        #     watchdog.error(alert_message)

        """
            TODO加入到celery tasks:
                1.快递接口访问（快递100或者是快递鸟接口访问）
                2.发送邮件
        """
       # if is_100:
       #      mall_signals.post_ship_send_request_to_kuaidi.send(sender=Order, order=order)
       #  from webapp.handlers import event_handler_util
       #  from utils import json_util
       #  event_data = {'order':json.dumps(Order.objects.get(id=order_id).to_dict(),cls=json_util.DateEncoder)}
       #  event_handler_util.handle(event_data, 'send_order_email')

        return True, ''