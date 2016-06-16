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

        #order_status_logs = OrderStatusLogInfo.from_order({'order': order}).logs
        #order_operation_logs = OrderOperationLogInfo.from_order({'order': order, 'child_orders': child_orders})

        order_info = order.to_dict('express_details', 'ship_area')
        order_info['product'] = products
        return order_info