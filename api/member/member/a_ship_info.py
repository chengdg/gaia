# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member
from business.common.page_info import PageInfo
from business.member.encode_member_service import EncodeMemberService

class AShipInfo(api_resource.ApiResource):
    """
    会员集合
    """
    app = "member"
    resource = "ship_info"

    @param_required(['corp_id', 'member_id', 'receiver_name', 'phone', 'address', 'area', 'is_selected:bool'])
    def put(args):
        corp = args['corp']

        ship_info = corp.modify_member_service.add_ship_info(args['member_id'], args)

        return {
            'id': ship_info.id
        }
