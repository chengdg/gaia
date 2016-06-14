# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order import Order
from business.mall.order_product_relation import OrderProductRelation
from business.mall.coupon.coupon import Coupon
from business.mall.coupon.coupon_rule import CouponRule
from business.mall.promotion.promotion import Promotion
from business.mall.promotion.product_has_promotion import ProductHasPromotion
from business.mall.order_status_log_info import OrderStatusLogInfo
from business.mall.order_operation_log_info import OrderOperationLogInfo
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
        products = order.products

        group_products = {}
        supplier_info = {}
        for product in products:
            key = "%d-%d" % (product['supplier'], product['supplier_user_id'])
            if key in group_products: group_products[key].append(product)
            else: group_products[key] = [product]
            if key not in supplier_info: supplier_info[key] = product['supplier_store_name']

        # 商品的积分和优惠券信息
        for product in products:
            if 'integral_count' in product and product['integral_count'] > 0:
                order.integral = None

        coupon = Coupon.get_coupon_by_id({'id': order.coupon_id})
        if coupon:
            coupon_rule = CouponRule.from_id({'id': coupon.coupon_rule_id})
            coupon.limit_product = coupon_rule.limit_product

            coupon_promotion = Promotion.from_detail_id({'detail_id': coupon_rule.id})
            product_has_promotion = ProductHasPromotion.from_promotion_id({'promotion_id': coupon_promotion.id})
            coupon_product_id = -1
            if len(product_has_promotion) > 0:
                coupon_product_id = product_has_promotion[0].product_id

            for product in order.products:
                if coupon.product_id == product['id']:
                    product['has_coupon'] = True
                    break
        child_orders = order.child_order
        order_status_logs = OrderStatusLogInfo.from_order({'order': order}).logs
        order_operation_logs = OrderOperationLogInfo.from_order({'order': order, 'child_orders': child_orders})
        order_info = AOrderDetail.to_dict(order)
        order_info['products'] = group_products

        child_orders_data = {}
        for child_order in child_orders:
            child_order = child_order.to_dict(
                'express_details',
                'is_group_buy',
                'number',
                'ship_area',
                'pay_interface_name',
                'save_money',
                'pay_money',
                'total_price',
                'action',
                'is_sub',
                'has_sub_order')
            key = "%d-%d" % (child_order['supplier'], child_order['supplier_user_id'])
            if key in child_orders_data: child_orders_data[key].append(child_order)
            else: child_orders_data[key] = [child_order]

        return {
            "order": order_info,
            "child_orders": child_orders_data,
            "order_status_logs": order_status_logs,
            "order_operation_logs": order_operation_logs,
            "supplier_info": supplier_info
        }

    @staticmethod
    def to_dict(order):
        order_dict = order.to_dict(
            'express_details',
            'is_group_buy',
            'number',
            'ship_area',
            'pay_interface_name',
            'save_money',
            'pay_money',
            'total_price',
            'action',
            'is_sub',
            'has_sub_order'
            )
        api_keys = [
            "number",
            "buyer_name",
            "coupon_money",
            "integral",
            "ship_area",
            "member_grade_id",
            "edit_money",
            "total_price",
            "save_money",
            "pay_money",
            "action",
            "id",
            "is_sub",
            "pay_interface_name",
            "ship_name",
            "has_sub_order",
            "product_price",
            "member_grade_discount",
            "supplier",
            "express_details",
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
            "bill_type",
            "bill",
            "delivery_time",
            "is_group_buy"
        ]

        data = {}
        for key in api_keys:
            data[key] = order_dict.get(key)
        return data

