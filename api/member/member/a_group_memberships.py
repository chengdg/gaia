# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member

class AGroupMemberships(api_resource.ApiResource):
    """
    会员的分组成员资格
    """
    app = "member"
    resource = "group_memberships"

    @param_required(['corp_id', 'member_group_ids:json', 'member_id'])
    def put(args):
        corp = args['corp']
        member = corp.member_repository.get_member_by_id(args['member_id'])
        member.join_groups(args['member_group_ids'])
        
        return {}
