# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member

class AGradeMemberships(api_resource.ApiResource):
    """
    会员的等级成员资格
    """
    app = "member"
    resource = "grade_memberships"

    @param_required(['corp_id', 'member_grade_id', 'member_ids:json'])
    def post(args):
        corp = args['corp']
        corp.modify_member_service.update_grade_for_members(args['member_ids'], args['member_grade_id'])
        
        return {}
