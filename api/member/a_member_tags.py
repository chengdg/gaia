# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.member.member_tags import MemberTag
from business.member.member_tags_factory import MemberTagFactory
from business.account.user_profile import UserProfile

class AMemberTags(api_resource.ApiResource):
    """
    会员分组
    """
    app = 'member'
    resource = 'member_tags'

    @param_required(['member_tag_id', 'name'])
    def put(args):
        '''
            更新分组名称
        '''
        print '-------------====================', args
        member_tag = MemberTag.from_id({'member_tag_id': args['member_tag_id']})
        count = 0
        if member_tag:
            count = member_tag.update_member_tag_name(args['member_tag_id'], args['name'])
        return {
            'count': count
        }
    @param_required(['owner_id','name'])
    def post(args):
        '''
        创建会员分组
        '''
        user_profile = UserProfile.from_user_id({'user_id':args['owner_id']})
        if user_profile:
             member_tag= MemberTagFactory.save({'webapp_id':user_profile.webapp_id, 'name': args['name']})
        return {
            'member_tag': member_tag
        }
