# -*- coding: utf-8 -*-
"""
优惠券的使用限制
"""
from datetime import datetime

from db.mall import promotion_models
from business import model as business_model

from db.mall import promotion_models


class CouponUsingLimit(business_model.Model):
    """
    优惠券使用限制
    """
    __slots__ = (
        'is_no_order_user_only',
        'is_for_specific_products',
        'product_ids',
        'has_valid_restriction',
        'valid_restrictions'
    )

    def __init__(self, valid_restrictions, is_no_order_user_only, product_ids):
        self.has_valid_restriction = (valid_restrictions != -1)
        self.valid_restrictions = valid_restrictions
        self.is_no_order_user_only = is_no_order_user_only
        self.is_for_specific_products = (product_ids != '-1')
        self.product_ids = product_ids.split(',')


