# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from db.express import models as express_models
from db.account import models as account_models
from util import regional_util

from business.mall.order_products import OrderProducts
from business.mall.express import util as express_util
from business.tools.express_detail import ExpressDetail
from business.mall.order_operation_log_info import OrderOperationLogInfo

class Order(business_model.Model):
    """
    订单
    """

    __slots__ = (
        'id',
        'order_id',
        'type',
        'pay_interface_type',
        'payment_time',
        'final_price',
        'product_price',
        'product_count',

        'ship_name',
        'ship_tel',
       # 'ship_area',
        'ship_address',
        'bill_type',
        'bill',

        'postage',
        'integral',
        'integral_money',
        'coupon_money',
        'edit_money',

        'coupon_id',
        'raw_status',
        'status',
        'origin_order_id',
        'express_company_name',
        'express_number',
        'customer_message',
        'promotion_saved_money',

        'created_at',
        'update_at',
        'leader_name',

        'supplier',
        'integral_each_yuan',
        'webapp_id',
        'webapp_user_id',
        'member_id',
        'member_grade_id',
        'member_grade_discount',
        'buyer_name',

        'weizoom_card_money',
        'delivery_time', # 配送时间字符串
        'is_first_order',
        'supplier_user_id',
        'total_purchase_price',
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            model.product_count = 0
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        order = Order(model)
        return order

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        order_db_model = mall_models.Order.select().dj_where(id=args['id'])
        if order_db_model.first():
            return Order(order_db_model.first())
        else:
            return None

    @staticmethod
    @param_required(['ids'])
    def from_ids(args):
        order_models = list(mall_models.Order.select().dj_where(id__in=args['ids']))
        order_models.sort(lambda x,y: cmp(y.id, x.id))
        return [Order(order_model) for order_model in order_models]

    @staticmethod
    @param_required(['origin_id'])
    def from_origin_id(args):
        order_db_models = mall_models.Order.select().dj_where(origin_order_id=args['origin_id'])
        return [Order(order_model) for order_model in order_db_models]

    @staticmethod
    @param_required(['order_ids'])
    def from_order_ids(args):
        order_models = mall_models.Order.select().dj_where(order_id__in=args['order_ids'])
        return [Order(order_model) for order_model in order_models]

    @staticmethod
    @param_required(['order_id'])
    def from_order_id(args):
        order_db_model = mall_models.Order.select().dj_where(order_id=args['order_id']).first()
        if order_db_model:
            return Order(order_db_model)
        else:
            return None

    @staticmethod
    @param_required(['supplier_ids']) #供货商
    def from_suppliers(args):
        order_db_models = mall_models.Order.select().dj_where(supplier__in=args['supplier_ids'])
        return [Order(order_model) for order_model in order_db_models]

    @staticmethod
    @param_required(['owner_id'])  #商品所属账号的user id ,获取此用户下所有订单列表
    def from_owner_id(args):
        user_db_model = account_models.User.select().dj_where(id=args['owner_id']).first()
        if user_db_model:
            userprofile_obj = account_models.UserProfile.select().dj_where(user=user_db_model).first()
            if userprofile_obj:
                orders = mall_models.Order.select().dj_where(webapp_id=userprofile_obj.webapp_id)
                if orders.count() != 0:

                    return [Order(order) for order in orders], orders
                return None, None
            else:
                return None, None
        else:
            return None, None

    @staticmethod
    def from_filter_params(args):      # 获取订单列表时用到，不要随便用
        print 'filter_--------====================', args
        filter_params = args['db_filter_params']
        orders_select_query = args['orders_select_query']
        special_filter_param = args['special_filter_param']
        filter_datetime_param = args['filter_datetime_param']
        other_params = args['other_params']
        order_list = []
        if filter_datetime_param:
            date_interval_type = filter_datetime_param['date_interval_type']
            if  date_interval_type == '1':  # 下单时间
                filter_params.update({
                    'created_at__gte': filter_datetime_param['_begin'], 
                    'created_at__lt': filter_datetime_param['_end']})
            elif date_interval_type == '2':  # 付款时间
                filter_params.update({
                    'payment_time__gte': filter_datetime_param['_begin'], 
                    'payment_time__lt': filter_datetime_param['_end']}) 
            elif  date_interval_type == '3': # 发货时间
                order_operation_log_info = OrderOperationLogInfo.empty_order_operation_log_info()
                orders_operation_log_info_ids = order_operation_log_info.get_orders_operation(orders_select_query, start_time=filter_datetime_param['_begin'], end_time=filter_datetime_param['_end'], action="订单发货")
                if not orders_operation_log_info_ids:
                    orders_operation_log_info_ids.append('')
                filter_params.update({'order_id__in': orders_operation_log_info_ids})
            elif  date_interval_type == '4': # 退款时间
                pass
            elif date_interval_type == '5': #退款完成时间
                pass
            elif date_interval_type == '6': # 订单完成时间
                pass
            elif date_interval_type == '7': # 订单取消时间
                pass
            else:
                pass

        elif 'is_used_weizoom_card' in special_filter_param:
                if special_filter_param['is_used_weizoom_card']:
                    # orders_select_query = orders_select_query.where(mall_models.Order.weizoom_card_money>0)
                    filter_params.update({'weizoom_card_money__gt': 0})
                else:
                    special_filter_param.pop('is_used_weizoom_card')
        print filter_params
        orders = orders_select_query.filter(**filter_params) if len(filter_params) != 0 else orders_select_query
        if 'sort_attr' in other_params:
            if '-' in other_params['sort_attr']:
                orders = orders.order_by(mall_models.Order.created_at.desc())
        if orders.count() != 0:
            for order in orders:
                order_obj = Order(order)
                flag = False
                if 'product_name' in special_filter_param:
                    for product in order_obj.products:
                        if  special_filter_param['product_name'] in product['name']:
                            flag = True
                            break
                if flag:
                    order_list.append(order_obj)

                if not special_filter_param:
                    order_list.append(order_obj)
            return order_list
        else:
            return None

    @property
    def is_group_buy(self):
        if not self.context.get('_is_group_buy'):
            self.context['_is_group_buy'] = bool(mall_models.OrderHasGroup.select().dj_where(order_id=self.order_id).first())

        return self.context['_is_group_buy']

    @is_group_buy.setter
    def is_group_buy(self, value):
        self.context['_is_group_buy'] = value

    @property
    def is_used_weizoom_card(self):
        return float(self.context['db_model'].weizoom_card_money) > 0

    @property
    def express_details(self):
        """
        [property] 订单的物流详情列表

        @return ExpressDetail对象list

        @see Weapp的`weapp/mall/models.py`中的`get_express_details()`
        """
        # 为了兼容有order.id的方式
        db_details = express_models.ExpressDetail.select().dj_where(order_id=self.id).order_by(-express_models.ExpressDetail.display_index)
        if db_details.count() > 0:
            detail_models = [ExpressDetail(detail) for detail in db_details]
            details = [{'ftime': model.ftime, 'context': model.context} for model in models]
            #return list(details)
            return details

        logging.info("express_company_name:{}, express_number:{}".format(self.express_company_name, self.express_number))
        expresses = express_models.ExpressHasOrderPushStatus.select().dj_where(
                express_company_name = self.express_company_name,
                express_number = self.express_number
            )
        if expresses.count() == 0:
            logging.info("No proper ExpressHasOrderPushStatus records.")
            return []

        try:
            express = expresses[0]
            logging.info("express: {}".format(express.id))
            db_details = express_models.ExpressDetail.select().dj_where(express_id=express.id).order_by(-express_models.ExpressDetail.display_index)
            detail_models = [ExpressDetail(detail) for detail in db_details]
            details = [{'ftime': model.ftime, 'context': model.context} for model in models]
        except Exception as e:
            logging.error(u'获取快递详情失败，order_id={}, case:{}'.format(self.id, str(e)))
            details = []
        return details

    @property
    def ship_area(self):
        db_model = self.context['db_model']
        return regional_util.get_str_value_by_string_ids(db_model.area)

    @property
    def products(self):
        """
        订单中的商品，包含商品的信息
        """
        products = self.context.get('products', None)
        if not products:
            #try:
            products = OrderProducts.get_for_order({'order': self }).products
            # except:
            #     import sys
            #     a, b, c = sys.exc_info()
            #     print a
            #     print b
            #     import traceback
            #     traceback.print_tb(c)
            self.context['products'] = products

        return products


    @property
    def formated_express_company_name(self):
        return  u'%s快递' % express_util.get_name_by_value(self.express_company_name) if self.express_company_name  else ''

    @property
    def child_order_count(self):
        if self.origin_order_id < 0:
            return mall_models.Order.select().dj_where(origin_order_id=self.id).count()
        return 0

    @property
    def is_sub_order(self):
        return self.origin_order_id > 0

    def order_handle_filter(self, action=None):
        order_operation_log_info = OrderOperationLogInfo.empty_order_operation_log_info()
        order_operation_log_info_obj = order_operation_log_info.from_order_id_action(self.context['db_model'].order_id, action)
        return order_operation_log_info_obj       

    @property
    def order_cancel(self):
        return self.order_handle_filter(action='取消订单')

    @property
    def order_refound_time(self):
        return self.order_handle_filter(action='退款')

    @property
    def order_refound_finish_time(self):
        return self.order_handle_filter(action='退款完成')

    @property
    def  fackorders(self):
        fackorders = mall_models.Order.select().dj_where(origin_order_id=self.context['db_model'].id)
        if fackorders.count() != 0:
            return [Order(order) for order in fackorders]
        else:
            return None

    @property
    def is_fackorder(self):
        return self.context['db_model'].is_sub_order
    @property
    def is_has_fackorder(self):
        return self.context['db_model'].has_sub_order

    @property
    def get_status_text(self):
        return self.context['db_model'].get_status_text()

    @property
    def get_str_area(self):
        return self.context['db_model'].get_str_area

    @property
    def get_pay_money(self):
        # 订单总额order.final_price + order.weizoom_card_money
        return self.final_price + self.weizoom_card_money

    @property
    def get_save_money(self):
        # 优惠金额
        return 0

    @property
    def get_order_actions(self):
        '''
        所有action:
        ORDER_PAY_ACTION
        ORDER_SHIP_ACTION
        ORDER_FINISH_ACTION
        ORDER_CANCEL_ACTION
        ORDER_REFUNDIND_ACTION
        ORDER_UPDATE_PRICE_ACTION
        ORDER_UPDATE_EXPREDSS_ACTION
        ORDER_REFUND_SUCCESS_ACTION
        '''
        ORDER_PAY_ACTION = {
            'name': u'支付',
            'action': 'pay',
            'class_name': 'xa-pay',
            'button_class': 'btn-success'
        }
        ORDER_SHIP_ACTION = {
            'name': u'发货',
            'action': 'ship',
            'class_name': 'xa-order-delivery',
            'button_class': 'btn-danger'
        }
        ORDER_FINISH_ACTION = {
            'name': u'标记完成',
            'action': 'finish',
            'class_name': 'xa-finish',
            'button_class': 'btn-success'
        }
        ORDER_CANCEL_ACTION = {
            'name': u'取消订单',
            'action': 'cancel',
            'class_name': 'xa-cancelOrder',
            'button_class': 'btn-danger'
        }
        ORDER_REFUNDIND_ACTION = {
            'name': u'申请退款',
            'action': 'return_pay',
            'class_name': 'xa-refund',
            'button_class': 'btn-danger'
        }
        ORDER_UPDATE_PRICE_ACTION = {
            'name': u'修改价格',
            'action': 'update_price',
            'class_name': 'xa-update-price',
            'button_class': 'btn-danger'
        }
        ORDER_UPDATE_EXPREDSS_ACTION = {
            'name': u'修改物流',
            'action': 'update_express',
            'class_name': 'xa-order-delivery',
            'button_class': 'btn-danger'
        }
        ORDER_REFUND_SUCCESS_ACTION = {
            'name': u'退款成功',
            'action': 'return_success',
            'class_name': 'xa-refundSuccess',
            'button_class': 'btn-danger'
        }
        PAY_INTERFACE_ALIPAY = mall_models.PAY_INTERFACE_ALIPAY
        PAY_INTERFACE_TENPAY = mall_models.PAY_INTERFACE_TENPAY
        PAY_INTERFACE_WEIXIN_PAY = mall_models.PAY_INTERFACE_WEIXIN_PAY
        PAY_INTERFACE_COD = mall_models.PAY_INTERFACE_COD
        PAY_INTERFACE_PREFERENCE = mall_models.PAY_INTERFACE_PREFERENCE
        PAY_INTERFACE_BEST_PAY = mall_models.PAY_INTERFACE_BEST_PAY
        PAY_INTERFACE_WEIZOOM_COIN = mall_models.PAY_INTERFACE_WEIZOOM_COIN

        result = []
        order = self.context['db_model']
        status = order.status
        if status == mall_models.ORDER_STATUS_NOT:
            result = [ORDER_PAY_ACTION, ORDER_UPDATE_PRICE_ACTION, ORDER_CANCEL_ACTION]
        elif status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_BEST_PAY]:
                result = [ORDER_SHIP_ACTION, ORDER_REFUNDIND_ACTION]
            else:
                result = [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
        elif status == mall_models.ORDER_STATUS_PAYED_SHIPED:
            actions = []
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_BEST_PAY]:
                if order.express_company_name:
                    actions = [ORDER_FINISH_ACTION, ORDER_UPDATE_EXPREDSS_ACTION, ORDER_REFUNDIND_ACTION]
                else:
                    actions = [ORDER_FINISH_ACTION, ORDER_REFUNDIND_ACTION]
            else:
                if order.express_company_name:
                    actions = [ORDER_FINISH_ACTION, ORDER_UPDATE_EXPREDSS_ACTION, ORDER_CANCEL_ACTION]
                else:
                    actions = [ORDER_FINISH_ACTION, ORDER_CANCEL_ACTION]
            result = actions
        elif status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_BEST_PAY]:
                if order.express_company_name:
                    result = [ORDER_REFUNDIND_ACTION, ORDER_UPDATE_EXPREDSS_ACTION]
                else:
                    result = [ORDER_REFUNDIND_ACTION]
            else:
                result = [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
        elif status == mall_models.ORDER_STATUS_SUCCESSED:
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_BEST_PAY,
                                            PAY_INTERFACE_COD]:
                result = [ORDER_REFUNDIND_ACTION]
            else:
                result = [ORDER_CANCEL_ACTION]
        # 团购订单去除订单取消，订单退款
        if self.is_group_buy:
            result = filter(lambda x: x not in [ORDER_CANCEL_ACTION, ORDER_REFUNDIND_ACTION], result)
        return result





