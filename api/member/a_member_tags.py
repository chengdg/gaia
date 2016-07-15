# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.member.member_tags import MemberTag

class AMemberTags(api_resource.ApiResource):
    """
    会员分组
    """
    app = 'member'
    resource = 'member_tags'

    @param_required('member_tag_id', 'name')
    def put(args):
        '''
            更新分组名称
        '''
        member_tag = MemberTag.from_id({'member_tag_id': args['member_tag_id']})
        count = 0
        if member_tag:
            count = member_tag.update_member_tag_name(args['member_tag_id', args['name']])
        else:
            return {
                'count': count
            }