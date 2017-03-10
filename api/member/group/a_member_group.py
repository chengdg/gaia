# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member_tag import MemberTag
from business.member.member import Member


class AMemberGroup(api_resource.ApiResource):
    """
    会员分组
    """
    app = "member"
    resource = "member_group"

    @param_required(['corp_id', 'name'])
    def put(args):
        member_tag = MemberTag.create(args)
        
        return {
            'id': member_tag.id
        }

    @param_required(['corp_id', 'id', 'name'])
    def post(args):
        corp = args['corp']
        member_tag = corp.member_tag_repository.get_member_tag_by_id(args['id'])
        member_tag.update({
            'name': args['name']
        })
        
        return {}

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        corp.member_tag_repository.delete_member_tag(args['id'])
        
        return {}
