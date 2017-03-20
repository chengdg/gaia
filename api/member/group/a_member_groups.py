# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.social_account import SocialAccount
from business.member.member import Member


class AMemberGroups(api_resource.ApiResource):
    """
    会员分组集合
    """
    app = "member"
    resource = "member_groups"

    @param_required(['corp_id', 'with_member_count:bool'])
    def get(args):
        corp = args['corp']
        member_tags = corp.member_tag_repository.get_member_tags()

        datas = []
        for member_tag in member_tags:
            data = {
                'id': member_tag.id,
                'name': member_tag.name
            }
            if args['with_member_count']:
                data['member_count'] = member_tag.member_count
            datas.append(data)
        
        return {
            'member_groups': datas
        }
