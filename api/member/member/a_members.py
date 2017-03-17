# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member
from business.common.page_info import PageInfo
from business.member.encode_member_service import EncodeMemberService

class AMembers(api_resource.ApiResource):
    """
    会员集合
    """
    app = "member"
    resource = "members"

    @param_required(['corp_id', '?filters:json'])
    def get(args):
        corp = args['corp']

        target_page = PageInfo.create({
            "cur_page": int(args.get('cur_page', 1)),
            "count_per_page": int(args.get('count_per_page', 10))
        })

        filters = args.get('filters', {})
        members, pageinfo = corp.member_repository.get_members(target_page, filters=filters)

        encode_member_service = EncodeMemberService.get(corp)
        datas = []
        for member in members:
            #base_info = encode_product_service.get_base_info(product)
            
            data = {
                'id': member.id,
                'name': member.username,
                'grade': encode_member_service.get_grade_info(member),
                'groups': encode_member_service.get_groups_info(member),
                'social_info': encode_member_service.get_social_info(member),
                'consume_info': encode_member_service.get_consume_info(member),
                'subscribe_info': encode_member_service.get_subscribe_info(member),
            }

            datas.append(data)

        return {
            'pageinfo': pageinfo.to_dict(),
            'members': datas
        }
