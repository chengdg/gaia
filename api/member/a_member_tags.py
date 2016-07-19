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

    @param_required(['member_tag_ids', 'name'])
    def put(args):
        '''
            更新分组名称
        '''
        member_tag_ids = filter( lambda c: c, args['member_tag_ids'].split(','))
        try:
            id_values = json.loads(args['name'])
        except :
            id_values = {}
            for x in member_tag_ids:
                id_values[x] = args['name']
        count = 0
        for member_tag_id in member_tag_ids:
            member_tag = MemberTag.from_id({'member_tag_id': member_tag_id})
            if not member_tag:
                return {
                    'msg': u'会员分组id {} 不存在'.format(member_tag_id)
                }
            else:
                count += member_tag.update_member_tag_name(member_tag_id, id_values[member_tag_id])
        return {
            'count': count
        }
    @param_required(['webapp_id','name'])
    def post(args):
        '''
        创建会员分组
        '''
        # user_profile = UserProfile.from_user_id({'user_id':args['owner_id']})
        # if user_profile:
        print 'args===============================', args
        params = {'webapp_id': args['webapp_id'], 'name': args['name']}
        member_tags = []
        if args.get('id', None):
            id_values = json.loads(args['name'])
            for member_tag_id in filter(lambda x: x, args['id'].split(',')):
                params.update({'id': member_tag_id, 'name': id_values[member_tag_id]})
                member_tags.append(MemberTagFactory.save(params))
        else:
                member_tags.append(MemberTagFactory.save(params))
        return {
            'member_tags': member_tags
        }

    @param_required(['webapp_id' ,'member_tag_ids'])
    def delete(args):
        '''
        删除会员分组
        '''
        member_tag_ids = filter(lambda x: x, args['member_tag_ids'].split(','))
        delete_member_tags = []
        for member_tag_id in member_tag_ids:
            member_tag = MemberTag.from_id({'member_tag_id': member_tag_id})
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
        count = member_tag.delete_from_ids(member_tag_ids)
        for m in members_in_member_has_tags:
            if len(MemberHasTag.from_member({'member': m.member}))==0:
                MemberHasTagFactory.save({'member': m.member, 'member_tag': member_tag_default_obj})
        return {
            'count': count
        }

