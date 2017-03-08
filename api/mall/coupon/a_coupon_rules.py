# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class ACouponRules(api_resource.ApiResource):
    """
    正在进行的促销活动集合
    """
    app = 'coupon'
    resource = 'coupon_rules'

    @param_required(['corp_id', '?filters:json'])
    def get(args):
        target_page = PageInfo.create({
            "cur_page": int(args.get('cur_page', 1)),
            "count_per_page": int(args.get('count_per_page', 10))
        })

        corp = args['corp']
        filters = args.get('filters', {})
        coupon_rules, pageinfo = corp.coupon_rule_repository.get_coupon_rules(filters, target_page)

        datas = []
        for coupon_rule in coupon_rules:
            using_limit = coupon_rule.using_limit
            data = {
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

            datas.append(data)

        return {
            'pageinfo': pageinfo.to_dict(),
            'coupon_rules': datas
        }

    @param_required(['corp_id', 'ids'])
    def delete(args):
        corp = args['corp']
        promotion_ids = json.loads(args['ids'])
        corp.promotion_repository.disable_promotions(promotion_ids)
        return {}
