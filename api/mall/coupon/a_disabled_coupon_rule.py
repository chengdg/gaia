# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.coupon.coupon_rule import CouponRule


class ADisabledCouponRule(api_resource.ApiResource):
    """
    失效的优惠券规则
    """
    app = 'coupon'
    resource = 'disabled_coupon_rule'

    @param_required(['corp_id', 'id'])
    def put(args):
        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.get_coupon_rule_by_id(args['id'])
        coupon_rule.disable()

        return {}