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
from business.mall.order_status_log_info import OrderStatusLogInfo
from business.account.user_profile import UserProfile


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
        'owner_id',
        'store_name'

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
                return [], None
            else:
                return [], None
        else:
            return [], None

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


        elif 'is_used_weizoom_card' in special_filter_param:
                if special_filter_param['is_used_weizoom_card']:
                    # orders_select_query = orders_select_query.where(mall_models.Order.weizoom_card_money>0)
                    filter_params.update({'weizoom_card_money__gt': 0})
                else:
                    special_filter_param.pop('is_used_weizoom_card')
        print filter_params
        if not orders_select_query:
            return []
        orders = orders_select_query.filter(**filter_params).order_by('-created_at') if len(filter_params) != 0 else orders_select_query
        def order_status_log(to_status, start_time, end_time):
            o_d = []
            for order in orders:
                order_status_log_infos = mall_models.OrderStatusLog.select().dj_where(order_id=order.order_id, 
                        to_status=to_status, 
                        created_at__gte=start_time, 
                        created_at__lt=end_time)
                if  order_status_log_infos.count() != 0:
                    o_d.append(Order(order))
            return o_d

        if filter_datetime_param:
            date_interval_type = filter_datetime_param['date_interval_type']
            if  date_interval_type == '4': # 退款时间
                return order_status_log(mall_models.ORDER_STATUS_REFUNDING, filter_datetime_param['_begin'], filter_datetime_param['_end'])
            elif date_interval_type == '5': #退款完成时间
                return order_status_log(mall_models.ORDER_STATUS_REFUNDED, filter_datetime_param['_begin'], filter_datetime_param['_end'])
            elif date_interval_type == '6': # 订单完成时间
                return order_status_log(mall_models.ORDER_STATUS_SUCCESSED, filter_datetime_param['_begin'], filter_datetime_param['_end'])
            elif date_interval_type == '7': # 订单取消时间
                return order_status_log(mall_models.ORDER_STATUS_CANCEL, filter_datetime_param['_begin'], filter_datetime_param['_end'])
            else:
                pass                   
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
            details = [{'ftime': model.ftime, 'context': model.context} for model in db_details]
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
            details = [{'ftime': model.ftime, 'context': model.context} for model in db_details]
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
    def order_finish_time(self):
        order_status_log_info = OrderStatusLogInfo(self)
        print order_status_log_info

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

    @staticmethod
    def search(product_ids=None, page=1, per_count_page=15, supplier_ids=None, from_mall=None,
               order_create_start=None, order_create_end=None, order_status=None, order_id=None):
        """
        根据不同条件搜索订单
        """
        # 获取带运营平台的账户
        if order_id:
            orders = mall_models.Order.select().dj_where(order_id)
            results = [Order(order) for order in orders]
        # for o in results:
        #     o.owner_id = webapp_to_user_id.get(o.webapp_id)
        #     o.store_name = user_to_store_name.get(o.webapp_id)
            return results, 1
        if not product_ids:
            user_profile = UserProfile.from_webapp_type({'webapp_type': 2})
            if not user_profile:
                return None
            owner_id = user_profile[0].user_id
            # 商品池（新的池）的所有商品
            pool_products = mall_models.Product.select().dj_where(is_deleted=False,
                                                                  owner=owner_id)
            if supplier_ids:
                pool_products = pool_products.dj_where(supplier__in=supplier_ids)
            if from_mall:
                # 某个自营平台的商品订单
                temp_user_profile = UserProfile.from_webapp_id({'webapp_id': from_mall})
                product_pool = mall_models.ProductPool.select().dj_where(woid=temp_user_profile.user_id)
                mall_product_ids = [pro.product_id for pro in product_pool]
                pool_products = pool_products.dj_where(id__in=mall_product_ids)
            product_ids = [p.id for p in pool_products]

        order_products = mall_models.OrderHasProduct.select().dj_where(product_id__in=product_ids)
        order_ids = [o.order_id for o in order_products]
        orders = mall_models.Order.select().dj_where(id__in=order_ids)
        if order_status:
            orders = orders.dj_where(status=order_status)
        if order_create_start:
            orders = orders.dj_where(created_at__gte=order_create_start)
        if order_create_start:
            orders = orders.dj_where(created_at__lte=order_create_end)
        orders = orders.dj_where(origin_order_id__lte=0)
        # 获取所有自营平台的user_id和webapp_id的映射关系
        # TODO 优化成通用接口
        user_profiles = UserProfile.from_mall_type({'mall_type': 1})
        keys = [user.webapp_id for user in user_profiles]
        values = [user.user_id for user in user_profiles]
        store_names = [user.store_name for user in user_profiles]
        webapp_to_user_id = dict(zip(keys, values))
        user_id_to_webapp = dict(zip(values, keys))
        user_to_store_name = dict(zip(keys, store_names))
        if from_mall:

            orders = orders.dj_where(webapp_id=from_mall)
        count = orders.count()
        orders = orders.paginate(int(page), paginate_by=int(per_count_page))

        # 补充订单的一些其他数据
        # for o in orders:
        #     pass
        results = [Order(order) for order in orders]
        for o in results:
            o.owner_id = webapp_to_user_id.get(o.webapp_id)
            o.store_name = user_to_store_name.get(o.webapp_id)
        return results, count
