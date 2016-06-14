# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from db.express import models as express_models
from util import regional_util

from business.mall.order_products import OrderProducts
from business.mall.express import util as express_util


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
        if order_db_model.count() == 0:
            return None
        order = Order(order_db_model.first())
        #order.ship_area = regional_util.get_str_value_by_string_ids(order_db_model.area)
        return order

    @staticmethod
    @param_required(['ids'])
    def from_ids(args):
        orders = []
        order_models = list(mall_models.Order.select().dj_where(id__in=args['ids']))
        order_models.sort(lambda x,y: cmp(y.id, x.id))

        for order_model in order_models:
            order = Order(order_model)
            #order.ship_area = regional_util.get_str_value_by_string_ids(order_model.area)
            orders.append(order)
        return orders

    @staticmethod
    @param_required(['origin_id'])
    def from_origin_id(args):
        order_db_models = mall_models.Order.select().dj_where(origin_order_id=args['origin_id'])
        orders = []
        for order_model in order_db_models:
            order = Order(order_model)
            #order.ship_area = regional_util.get_str_value_by_string_ids(order_model.area)
            orders.append(order)
        return orders

    @staticmethod
    @param_required(['order_id'])
    def from_order_id(args):
        if mall_models.Order.select().dj_where(order_id=args['order_id']).count() == 0:
            return None
        order_db_model = mall_models.Order.select().dj_where(order_id=args['order_id']).first()
        order = Order(order_db_model)
        #order.ship_area = regional_util.get_str_value_by_string_ids(order_db_model.area)
        return order

    @property
    def is_group_buy(self):
        if not self.context.get('_is_group_buy'):
            self.context['_is_group_buy'] = bool(mall_models.OrderHasGroup.select().dj_where(order_id=self.order_id).first())

        return self.context['_is_group_buy']

    @is_group_buy.setter
    def is_group_buy(self, value):
        self.context['_is_group_buy'] = value

    @property
    def is_sub_order(self):
        """
        [property] 该订单是否是子订单
        """
        return self.origin_order_id > 0

    @property
    def has_sub_order(self):
        """
        [property] 该订单是否有子订单
        """
        return self.origin_order_id == -1 and self.status > mall_models.ORDER_STATUS_NOT

    @property
    def number(self):
        self.context['_number'] = 0
        self.context['_total_price'] = 0.0
        relations = mall_models.OrderHasProduct.select().dj_where(order_id=self.id)
        for relation in relations:
            self.context['_number'] += relation.number
            self.context['_total_price'] += relation.total_price
        return self.context['_number']

    @property
    def pay_interface_name(self):
        self.context['_pay_interface_name'] = mall_models.PAYTYPE2NAME.get(self.pay_interface_type, u'')
        return self.context['_pay_interface_name']

    @property
    def total_price(self):
        return self.context['_total_price']

    @property
    def pay_money(self):
        self.context['_pay_money'] = self.final_price + self.weizoom_card_money
        return self.context['_pay_money']

    @property
    def save_money(self):
        self.context['_save_money'] = self.context['_total_price'] + self.postage - (self.final_price + self.weizoom_card_money)
        return self.context['_save_money']

    @property
    def child_order(self):
        if self.origin_order_id != -1:
            return []
        order_models = mall_models.Order.select().dj_where(origin_order_id=self.id)
        child_orders = []
        for model in order_models:
            child_orders.append(Order(model))

        return child_orders

    # @property
    # def real_has_sub_order(self):
    #     """
    #     [property] 真正的该订单是否有子订单
    #     """
    #     return self.origin_order_id == -1

    # @property
    # def is_sub_order(self):
    #     """
    #     [property] 该订单是否是子订单
    #     """
    #     return self.origin_order_id > 0

    # def has_multi_sub_order(self):
    #     """
    #     [property] 该订单是否有超过一个子订单
    #     """
    #     return self.has_sub_order and len(self.get_sub_order_ids()) > 1

    # def get_sub_order_ids(self):
    #     if self.real_has_sub_order:
    #         orders = mall_models.Order.select().dj_where(origin_order_id=self.id)
    #         sub_order_ids = [order.order_id for order in orders]
    #         return sub_order_ids
    #     else:
    #         return []




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
            details = [ExpressDetail(detail) for detail in db_details]
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
            details = [ExpressDetail(detail) for detail in db_details]
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
            products = OrderProducts.get_for_order({
                #'webapp_owner': self.context['webapp_owner'],
                #'webapp_user': self.context['webapp_user'],
                'order': self,
            }).products
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
    def group_products(self):
        pass

    @property
    def formated_express_company_name(self):
        return  u'%s快递' % express_util.get_name_by_value(self.express_company_name) if self.express_company_name  else ''

    @property
    def action(self):
        # TODO 后期把下面参数加到order的属性当中
        order = self
        is_refund=False
        is_detail_page=False
        is_list_parent=False
        mall_type=0
        multi_child_orders=False
        is_group_buying=False

        result = []
        if not is_refund:
            if order.status == mall_models.ORDER_STATUS_NOT:
                result = [mall_models.ORDER_PAY_ACTION, mall_models.ORDER_UPDATE_PRICE_ACTION, mall_models.ORDER_CANCEL_ACTION]
            elif order.status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
                if order.pay_interface_type in [mall_models.PAY_INTERFACE_ALIPAY, mall_models.PAY_INTERFACE_TENPAY, mall_models.PAY_INTERFACE_WEIXIN_PAY, mall_models.PAY_INTERFACE_BEST_PAY]:
                    result = [mall_models.ORDER_SHIP_ACTION, mall_models.ORDER_REFUNDIND_ACTION]
                else:
                    result = [mall_models.ORDER_SHIP_ACTION, mall_models.ORDER_CANCEL_ACTION]
            elif order.status == mall_models.ORDER_STATUS_PAYED_SHIPED:
                actions = []
                print  [mall_models.PAY_INTERFACE_ALIPAY, mall_models.PAY_INTERFACE_TENPAY, mall_models.PAY_INTERFACE_WEIXIN_PAY, mall_models.PAY_INTERFACE_BEST_PAY]
                if order.pay_interface_type in [mall_models.PAY_INTERFACE_ALIPAY, mall_models.PAY_INTERFACE_TENPAY, mall_models.PAY_INTERFACE_WEIXIN_PAY, mall_models.PAY_INTERFACE_BEST_PAY]:
                    if order.express_company_name:
                        actions = [mall_models.ORDER_FINISH_ACTION, mall_models.ORDER_UPDATE_EXPREDSS_ACTION, mall_models.ORDER_REFUNDIND_ACTION]
                    else:
                        actions = [mall_models.ORDER_FINISH_ACTION, mall_models.ORDER_REFUNDIND_ACTION]
                else:
                    if order.express_company_name:
                        actions = [mall_models.ORDER_FINISH_ACTION, mall_models.ORDER_UPDATE_EXPREDSS_ACTION, mall_models.ORDER_CANCEL_ACTION]
                    else:
                        actions = [mall_models.ORDER_FINISH_ACTION, mall_models.ORDER_CANCEL_ACTION]
                result = actions
            elif order.status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
                if order.pay_interface_type in [mall_models.PAY_INTERFACE_ALIPAY, mall_models.PAY_INTERFACE_TENPAY, mall_models.PAY_INTERFACE_WEIXIN_PAY, mall_models.PAY_INTERFACE_BEST_PAY]:
                    if order.express_company_name:
                        result = [mall_models.ORDER_REFUNDIND_ACTION, mall_models.ORDER_UPDATE_EXPREDSS_ACTION]
                    else:
                        result = [mall_models.ORDER_REFUNDIND_ACTION]
                else:
                    result = [mall_models.ORDER_SHIP_ACTION, mall_models.ORDER_CANCEL_ACTION]
            elif order.status == mall_models.ORDER_STATUS_SUCCESSED:
                if order.pay_interface_type in [mall_models.PAY_INTERFACE_ALIPAY, mall_models.PAY_INTERFACE_TENPAY, mall_models.PAY_INTERFACE_WEIXIN_PAY, mall_models.PAY_INTERFACE_BEST_PAY,
                                                mall_models.PAY_INTERFACE_COD]:
                    result = [mall_models.ORDER_REFUNDIND_ACTION]
                else:
                    result = [mall_models.ORDER_CANCEL_ACTION]
        elif is_refund:
            if order.status == mall_models.ORDER_STATUS_REFUNDING:
                result = [mall_models.ORDER_REFUND_SUCCESS_ACTION]
            elif order.status == mall_models.ORDER_STATUS_GROUP_REFUNDING:
                result = []

        # 订单列表页子订单
        able_actions_for_sub_order = [mall_models.ORDER_SHIP_ACTION, mall_models.ORDER_UPDATE_EXPREDSS_ACTION, mall_models.ORDER_FINISH_ACTION]

        # 订单详情页有子订单
        able_actions_for_detail_order_has_sub = [mall_models.ORDER_PAY_ACTION, mall_models.ORDER_SHIP_ACTION, mall_models.ORDER_UPDATE_EXPREDSS_ACTION,
                                                 mall_models.ORDER_FINISH_ACTION]

        # 订单列表页有子订单的父母订单
        able_actions_for_list_parent = [mall_models.ORDER_CANCEL_ACTION, mall_models.ORDER_REFUNDIND_ACTION, mall_models.ORDER_REFUND_SUCCESS_ACTION]

        # 同步订单操作
        sync_order_actions = [mall_models.ORDER_PAY_ACTION, mall_models.ORDER_UPDATE_PRICE_ACTION, mall_models.ORDER_SHIP_ACTION, mall_models.ORDER_UPDATE_EXPREDSS_ACTION, mall_models.ORDER_FINISH_ACTION]
        # print(order.order_id, order.is_sub_order, order.origin_order_id)
        # print(result)
        # 订单被同步后查看
        if not mall_type and order.supplier_user_id:
            result = filter(lambda x: x in sync_order_actions, result)
        # else:
        #     if order.is_sub_order:
        #         result = filter(lambda x: x in able_actions_for_sub_order, result)
        if not mall_type:
            if (order.supplier or order.supplier_user_id) and is_detail_page:
                result = filter(lambda x: x in able_actions_for_detail_order_has_sub, result)

        if is_list_parent:
            result = filter(lambda x: x in able_actions_for_list_parent, result)

        # 团购订单去除订单取消，订单退款
        if is_group_buying:
            result = filter(lambda x: x not in [mall_models.ORDER_CANCEL_ACTION, mall_models.ORDER_REFUNDIND_ACTION], result)

        if multi_child_orders:
            result = filter(lambda x: x not in able_actions_for_list_parent, result)

        self.context['_action'] = result
        return result