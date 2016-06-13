# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order import Order
from business.mall.order_product_relation import OrderProductRelation
from db.mall import models as mall_models

class AOrderDetail(api_resource.ApiResource):
    """
    订单列表
    """

    app = 'mall'
    resource = 'order_detail'

    @param_required(['order_id'])
    def get(args):
        order = Order.from_order_id({'order_id': args['order_id']})

        if not order:
            return {"order": None}


        # 订单商品
        # 商品的积分和优惠券信息
        # 订单的团购
        # 订单的详细信息
        # 子订单


        return {"order": AOrderDetail.to_dict(order)}

    @staticmethod
    def to_dict(order):
        order_dict = order.to_dict('latest_express_detail', 'products', 'is_group_buy', 'order_group_info')
        api_keys = [
            "buyer_name",
            "coupon_money",
            "integral",
            "ship_area",
            "member_grade_id",
            "edit_money",
            "id",
            "pay_interface_name",
            "ship_name",
            "has_sub_order",
            "has_multi_sub_order",
            "sub_orders",
            "product_price",
            "member_grade_discount",
            "supplier",
            "latest_express_detail",
            "type",
            "integral_each_yuan",
            "final_price",
            "status",
            "postage",
            "ship_address",
            "pay_interface_type",
            "order_id",
            "integral_money",
            "ship_tel",
            "origin_order_id",
            "coupon_id",
            "customer_message",
            "webapp_id",
            "promotion_saved_money",
            "express_number",
            "webapp_user_id",
            "products",
            "status_text",
            "created_at",
            "weizoom_card_money",
            "red_envelope",
            "red_envelope_created",
            "pay_info",
            "bill_type",
            "bill",
            "delivery_time",
            "is_group_buy",
            "order_group_info",
        ]

        data = {}
        for key in api_keys:
            data[key] = order_dict.get(key)
        return {
            "order": data
        }

