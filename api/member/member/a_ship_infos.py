# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member
from business.common.page_info import PageInfo
from business.member.encode_member_service import EncodeMemberService

class AShipInfos(api_resource.ApiResource):
    """
    会员的收货地址集合
    """
    app = "member"
    resource = "ship_infos"

    @param_required(['corp_id', 'member_id'])
    def get(args):
        corp = args['corp']

        member = corp.member_repository.get_member_by_id(args['member_id'])
        encode_member_service = EncodeMemberService.get(corp)
        ship_infos = encode_member_service.get_ship_infos(member)

        return {
            'ship_infos': ship_infos
        }
