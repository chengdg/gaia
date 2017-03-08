# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.coupon.coupon_rule import CouponRule


class ACouponRule(api_resource.ApiResource):
    """
    优惠券规则
    """
    app = 'coupon'
    resource = 'coupon_rule'

    @param_required(['corp_id', 'id'])
    def get(args):
        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.get_coupon_rule_by_id(args['id'])

        using_limit = coupon_rule.using_limit
        return {
            'id': coupon_rule.id,
            'name': coupon_rule.name,
            'money': coupon_rule.money,
            'coupon_count': coupon_rule.coupon_count,
            'receive_limit_count': coupon_rule.receive_limit_count,
            'remark': coupon_rule.remark,
            'note': coupon_rule.note,
            'valid_days': coupon_rule.valid_days,
            'status': coupon_rule.status,
            'remained_count': coupon_rule.remained_count,
            'receive_user_count': coupon_rule.receive_user_count,
            'receive_count': coupon_rule.receive_count,
            'use_count': coupon_rule.use_count,
            'start_date': coupon_rule.start_date.strftime('%Y-%m-%d %H:%M'),
            'end_date': coupon_rule.end_date.strftime('%Y-%m-%d %H:%M'),
            'created_at': coupon_rule.created_at.strftime('%Y-%m-%d %H:%M'),
            'using_limit': {
                'is_no_order_user_only': using_limit.is_no_order_user_only,
                'is_for_specific_products': using_limit.is_for_specific_products,
                'product_ids': using_limit.product_ids,
                'has_valid_restriction': using_limit.has_valid_restriction,
                'valid_restrictions': using_limit.valid_restrictions
            }
        }

    @param_required(['corp_id', 'name', 'money', 'coupon_count', 'receive_limit_count', 'start_date', 'end_date', 'remark', 'note', 'using_limit:json'])
    def put(args):
        corp = args['corp']
        coupon_rule = CouponRule.create(args)

        return {
            'id': coupon_rule.id
        }

    @param_required(['corp_id', 'id', '?name', '?remark', '?note'])
    def post(args):
        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.get_coupon_rule_by_id(args['id'])
        coupon_rule.update({
            "name": args['name'],
            "remark": args['remark'],
            'note': args['note']
        })

        return {}

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.delete_coupon_rule(args['id'])

        return {}