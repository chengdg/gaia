# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class ACoupons(api_resource.ApiResource):
    """
    优惠券集合
    """
    app = 'coupon'
    resource = 'coupons'

    @param_required(['corp_id', 'coupon_rule_id', 'count:int'])
    def put(args):
        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.get_coupon_rule_by_id(args['coupon_rule_id'])
        added_count = coupon_rule.add_coupons(args['count'])

        return {
            'count': added_count
        }

    @param_required(['corp_id', 'coupon_rule_id', '?filters:json'])
    def get(args):
        target_page = PageInfo.create({
            "cur_page": int(args.get('cur_page', 1)),
            "count_per_page": int(args.get('count_per_page', 10))
        })

        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.get_coupon_rule_by_id(args['coupon_rule_id'])
        filters = args.get('filters', {})
        coupons, pageinfo = corp.coupon_repository.get_coupons_for_rule(coupon_rule.id, filters, target_page)

        datas = []
        for coupon in coupons:
            using_limit = coupon_rule.using_limit
            data = {
                'id': coupon.id,
                'bid': coupon.bid,
                'status': coupon.display_status,
                'money': coupon.money,
                'start_time': coupon.start_time.strftime('%Y-%m-%d %H:%M'),
                'expired_time': coupon.expired_time.strftime('%Y-%m-%d %H:%M'),
                'created_at': coupon.created_at.strftime('%Y-%m-%d %H:%M'),
                'received_time': coupon.received_time.strftime('%Y-%m-%d %H:%M'),
                'receive_user': coupon.receive_user_name,
                'used_time': coupon.used_time.strftime('%Y-%m-%d %H:%M'),
                'use_user': coupon.use_user_name,
                'order_bid': coupon.order_bid,
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
            'coupons': datas
        }

    @param_required(['corp_id', 'ids:json'])
    def delete(args):
        corp = args['corp']
        corp.coupon_repository.delete_coupons(args['ids'])
        return {}
