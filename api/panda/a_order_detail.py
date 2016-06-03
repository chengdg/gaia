# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.tools.express_detail import ExpressDetail
from db.mall import models as mall_models

class AOrderDetail(api_resource.ApiResource):
    """
    订单列表
    """
    app = 'panda'
    resource = 'order_detail'

    @param_required(['order_id'])
    def get(args):
        """
        订单详情
        """
        order = Order.from_id({'id': args['order_id']})
        if not order:
            return {
                'order': {}
            }
        order_data = order.to_dict()
        order_has_product_relations = OrderProductRelation.get_for_order({'order_ids': [order.id]})

        products = []
        for relation in order_has_product_relations:
            products.append({
                'product_id': relation.product_id,
                'total_price': relation.total_price,
                'purchase_price': relation.purchase_price,
                'count': relation.number
            })
        order_data['products'] = products

        order_express_details = []
        if order.status > mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
            express_details = ExpressDetail.from_express_info({
                    'express_number': order.express_number,
                    'express_company_name': order.express_company_name
                })
            for detail in express_details:
                order_express_details.append({
                    'time': detail.time,
                    'context': detail.context
                })

        order_data['order_express_details'] = order_express_details
        return {
            'order': order_data
        }