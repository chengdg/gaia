# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.member.member import Member

class AMemberCoupons(api_resource.ApiResource):
    """
    会员优惠券集合
    """
    app = "member"
    resource = "coupons"

    @param_required(['corp_id', 'member_id'])
    def get(args):
        corp = args['corp']

        target_page = PageInfo.create({
            "cur_page": int(args.get('cur_page', 1)),
            "count_per_page": int(args.get('count_per_page', 10))
        })

        datas = []
        member = corp.member_repository.get_member_by_id(args['member_id'])
        coupons, pageinfo =  member.get_coupons(target_page)
        for coupon in coupons:
            datas.append({
                'id': coupon.id,
                'bid': coupon.bid,
                'money': coupon.money,
                'name': coupon.rule.name,
                'using_limit': coupon.using_limit,
                'received_time': coupon.received_time.strftime('%Y-%m-%d %H:%M'),
                'status': coupon.display_status,
                'order_bid': coupon.order_bid
            })

        return {
            'pageinfo': pageinfo.to_dict(),
            'coupons': datas
        }

    @param_required(['corp_id', 'member_ids:json', 'coupon_rule_id', 'count_per_member:int'])
    def put(args):
        corp = args['corp']
        coupon_rule = corp.coupon_rule_repository.get_coupon_rule_by_id(args['coupon_rule_id'])
        count, reason = coupon_rule.provide_to_members(args['member_ids'], args['count_per_member'])
        
        return {
            'count': count,
            'reason': reason
        }
