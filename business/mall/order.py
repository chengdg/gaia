# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
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
        'express_details',
        'customer_message',
        'promotion_saved_money',

        'created_at',
        'update_at',

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

    @property
    def save_money(self):
        self.context['_save_money'] = self.context['_total_price'] + self.postage - (self.final_price + self.weizoom_card_money)



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

    # def sub_orders(self):
    #     """
    #     拆单后的子订单信息
    #     """
    #     pass

    # def latest_express_detail(self):
    #     """
    #     [property] 订单的最新物流详情
    #     """
    #     details = self.express_details
    #     if details:
    #         return details[-1].to_dict()
    #     return None



    # @property
    # def products(self):
    #     """
    #     订单中的商品，包含商品的信息
    #     """
    #     products = self.context.get('products', None)
    #     if not products:
    #         try:
    #             products = OrderProducts.get_for_order({
    #                 'webapp_owner': self.context['webapp_owner'],
    #                 'webapp_user': self.context['webapp_user'],
    #                 'order': self,
    #             }).products
    #         except:
    #             import sys
    #             a, b, c = sys.exc_info()
    #             print a
    #             print b
    #             import traceback
    #             traceback.print_tb(c)

    #         self.context['products'] = products

    #     return products

    # @products.setter
    # def products(self, products):
    #     self.context['products'] = products

    # @property
    # def product_groups(self):
    #     return self.context['product_groups']

    # @product_groups.setter
    # def product_groups(self, product_groups):
    #     self.context['product_groups'] = product_groups

    # @property
    # def express_details(self):
    #     """
    #     [property] 订单的物流详情列表

    #     @return ExpressDetail对象list

    #     @see Weapp的`weapp/mall/models.py`中的`get_express_details()`
    #     """
    #     # 为了兼容有order.id的方式
    #     db_details = express_models.ExpressDetail.select().dj_where(order_id=self.id).order_by(-express_models.ExpressDetail.display_index)
    #     if db_details.count() > 0:
    #         details = [ExpressDetail(detail) for detail in db_details]
    #         #return list(details)
    #         return details

    #     logging.info("express_company_name:{}, express_number:{}".format(self.express_company_name, self.express_number))
    #     expresses = express_models.ExpressHasOrderPushStatus.select().dj_where(
    #             express_company_name = self.express_company_name,
    #             express_number = self.express_number
    #         )
    #     if expresses.count() == 0:
    #         logging.info("No proper ExpressHasOrderPushStatus records.")
    #         return []

    #     try:
    #         express = expresses[0]
    #         logging.info("express: {}".format(express.id))
    #         db_details = express_models.ExpressDetail.select().dj_where(express_id=express.id).order_by(-express_models.ExpressDetail.display_index)
    #         details = [ExpressDetail(detail) for detail in db_details]
    #     except Exception as e:
    #         logging.error(u'获取快递详情失败，order_id={}, case:{}'.format(self.id, str(e)))
    #         details = []
    #     return details

    # def order_group_info(self):
    #     order_has_group = mall_models.OrderHasGroup.select().dj_where(order_id=self.order_id).first()
    #     activity_url = ''
    #     if order_has_group:
    #         order_group_info = order_has_group.to_dict()
    #         if self.status == mall_models.ORDER_STATUS_NOT:
    #             activity_url = 'http://' + settings.WEAPP_DOMAIN + '/m/apps/group/m_group/?webapp_owner_id=' + str(self.context['webapp_owner'].id) + '&id=' + order_group_info['activity_id']
    #         else:
    #             url = GroupBuyOPENAPI['get_group_url']
    #             data = {
    #                 'woid': self.context['webapp_owner'].id,
    #                 'group_id': order_group_info['group_id']
    #             }
    #             is_success, group_url_info = microservice_consume(url=url,data=data)
    #             if is_success:
    #                 activity_url = 'http://' + settings.WEAPP_DOMAIN + group_url_info['group_url']
    #         order_group_info['activity_url'] = activity_url
    #         return order_group_info
    #     else:
    #         return {}

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
    def formated_express_company_name(self):
        return  u'%s快递' % express_util.get_name_by_value(self.express_company_name) if self.express_company_name  else ''