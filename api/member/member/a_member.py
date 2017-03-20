# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member

from business.member.encode_member_service import EncodeMemberService


class AMember(api_resource.ApiResource):
    """
    会员
    """
    app = "member"
    resource = "member"

    @param_required(['corp_id', 'id'])
    def get(args):
        corp = args['corp']
        member = corp.member_repository.get_member_by_id(args['id'])

        encode_member_service = EncodeMemberService.get(corp)
        data = {
            'id': member.id,
            'name': member.username,
            'thumbnail': member.thumbnail,
            'grade': encode_member_service.get_grade_info(member),
            'groups': encode_member_service.get_groups_info(member),
            'social_info': encode_member_service.get_social_info(member),
            'consume_info': encode_member_service.get_consume_info(member),
            'subscribe_info': encode_member_service.get_subscribe_info(member),
        }

        return data