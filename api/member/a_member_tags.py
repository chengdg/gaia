# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.member.member_tags import MemberTag
from business.member.member_tags_factory import MemberTagFactory
from business.account.user_profile import UserProfile
from business.member.member_has_tag import MemberHasTag
from business.member.member_has_tag_factory import MemberHasTagFactory


class AMemberTags(api_resource.ApiResource):
    """
    会员分组
    """
    app = 'member'
    resource = 'member_tags'
    
    @param_required([])
    def get(args):
        ''''

        '''
        if args.get('id', None) and args.get('webapp_id', None):
            opt = {'id':args['id'], 'webapp_id': args['webapp_id']}
            member_tags = MemberTag.from_webapp_id(opt)
        elif args.get('id', None):
            opt = {'id': args['id']}
            member_tags = MemberTag.from_id(opt)
        else:
            opt = {'webapp_id': args['webapp_id']}
            member_tags = MemberTag.from_webapp_id(opt)
        return {
            'member_tags': member_tags
        }

    @param_required(['id', 'webapp_id','name'])
    def put(args):
        '''
            更新分组名称
        '''
        member_tag = MemberTag.from_id({'id': args['id']})
        if not member_tag:
            return {
                'msg': u'会员分组id {} 不存在'.format(args['id'])
            } 
        count = member_tag.update_member_tag_name(args['id'],args['webapp_id'], args['name'])
        return {
            'count': count
        }
    @param_required(['webapp_id','name'])
    def post(args):
        '''
        创建会员分组
        '''
        if 'id' in args:
            opt = {'id': args['id'],'webapp_id': args['webapp_id'], 'name': args['name']}
        else:
            opt = {'webapp_id': args['webapp_id'], 'name': args['name']}
        member_tag = MemberTagFactory.save(opt)
        return {
            'member_tag': member_tag
        }

    @param_required(['webapp_id' ,'member_tag_ids'])
    def delete(args):
        '''
        删除会员分组
        '''
        print '========================',args
        member_tag_ids = [int(c) for c in filter(lambda x: int(x)!=0, args['member_tag_ids'].split(','))]
        delete_member_tags = []
        for member_tag_id in member_tag_ids:
            member_tag = MemberTag.from_id({'id': member_tag_id})
            if not member_tag:
                return {
                    'msg': u'会员分组id{}不存在'.format(member_tag_id)
                }
            else:
                delete_member_tags.append(member_tag)
        members_in_member_has_tags = MemberHasTag.from_member_tags({'member_tags': delete_member_tags})
        member_tag_default_obj = MemberTag.from_webapp_id({'webapp_id': args['webapp_id']})
        member_has_tag_instance = MemberHasTag.empty_member_has_tag()
        if members_in_member_has_tags:
            member_has_tag_instance.delete_from_ids([ member_has_tag.id for member_has_tag in members_in_member_has_tags])
        member_tag = MemberTag.empty_member_tags()
        count = member_tag.delete_from_ids(member_tag_ids)
        for m in members_in_member_has_tags:
            if len(MemberHasTag.from_member({'member': m.member}))==0:
                MemberHasTagFactory.save({'member': m.member, 'member_tag': member_tag_default_obj[0]})
        return {
            'count': count
        }

