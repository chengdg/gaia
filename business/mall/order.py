# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from util import regional_util

from business.mall.order_products import OrderProducts


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
        'edit_money',

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

        'supplier',
        'integral_each_yuan',
        'webapp_id',
        'webapp_user_id',
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
        # order_db_model = mall_models.Order.select().dj_where(id=args['id'])
        if mall_models.Order.select().dj_where(order_id=args['order_id']).count() == 0:
            return None
        order_db_model = mall_models.Order.select().dj_where(order_id=args['order_id']).first()
        order = Order(order_db_model)
        #order.ship_area = regional_util.get_str_value_by_string_ids(order_db_model.area)
        return order

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

    
    

