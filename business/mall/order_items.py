# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from business.mall.order_products import OrderProducts

class OrderItems(business_model.Model):
    """
    返回的订单详情的列表
    """
    __slots__ = (
        'items',
    )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    @param_required(['orders'])
    def get_for_order(args):
        order_items = OrderItems()
        data = order_items.__get_items_for_order(args['orders'])

        return order_items.items

    def __get_items_for_order(self, orders):
        """
        组织返回的订单数据
        """

        self.items = []
        for order in orders:
            products = OrderProducts.get_for_order({'order': order})
            self.items.append({

            })

