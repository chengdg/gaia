# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_state import OrderState
from business.tools.express_detail import ExpressDetail

class AOrder(api_resource.ApiResource):
    """
    订单
    """
    app = 'mall'
    resource = 'order'

    # @param_required(['ship_name', 'ship_address', 'ship_tel', 'order_type', 'xa-choseInterfaces'])
    # def put(args):
    #     """
    #     下单接口

    #     @param id 商
    @param_required(['order_id', "action", "operation_name"])
    def post(args):
        order_id = args['order_id']
        action = args['action']
        operation_name = args["operation_name"]

        order = OrderState.from_order_id({
            "order_id": order_id
            })
        if action == "finish":
            order.finish(operation_name)