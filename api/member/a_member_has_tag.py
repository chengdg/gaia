# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.member.member import Member
from business.member.member_tags  import MemberTag
from business.member.member_has_tag  import MemberHasTag
from business.member.member_has_tag_factory import MemberHasTagFactory


class AMemberHasTags(api_resource.ApiResource):
    """
    会员分组
    """
    app = 'member'
    resource = 'member_has_tag'

    @param_required(['member_id'])
    def put(args):
        '''
        会员修改分组
        '''
        print '-===========================', args
        member = Member.from_id({'id': args['member_id']})
        if  not args.get('member_tag_ids', None)  and member:
            member_tag_obj = MemberTag.from_webapp_id({'webapp_id': member.webapp_id})
            args['member_tag_ids'] = '{}'.format(member_tag_obj.id) 
        # import pdb
        # pdb.set_trace()
        member_tags = []
        for member_tag_id in filter(lambda x: x, args['member_tag_ids'].split(',')):
            member_tag = MemberTag.from_id({'member_tag_id': member_tag_id})
            if not member_tag:
                return {
                    'msg': u'会员分组 {} 不存在'.format(member_tag_id)
                }
            else:
                member_tags.append(member_tag)
        # import pdb
        # pdb.set_trace()
        if member:
            count = MemberHasTag.delete_member_has_tags({'member': member})
                
            for member_tag in member_tags:
                    MemberHasTagFactory.save({'member':member, 'member_tag': member_tag})
        return {
            'msg': 'successed'
        }
