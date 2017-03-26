# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member

from business.member.encode_member_service import EncodeMemberService


class AMember(api_resource.ApiResource):
    """
    会员
    """
    app = "member"
    resource = "member"

    @param_required(['corp_id', 'id', '?fill_options:json'])
    def get(args):
        corp = args['corp']
        member = corp.member_repository.get_member_by_id(args['id'])

        encode_member_service = EncodeMemberService.get(corp)
        data = {
            'id': member.id,
            'name': member.username,
            'thumbnail': member.thumbnail,
            'basic_info': encode_member_service.get_basic_info(member),
            'grade': encode_member_service.get_grade_info(member),
            'groups': encode_member_service.get_groups_info(member),
            'social_info': encode_member_service.get_social_info(member),
            'consume_info': encode_member_service.get_consume_info(member),
            'subscribe_info': encode_member_service.get_subscribe_info(member)
        }

        fill_options = args.get('fill_options', {})
        if 'with_ship_info' in fill_options:
            data['ship_infos'] = encode_member_service.get_ship_infos(member)

        return data

    @param_required(['corp_id', 'id', '?member_grade_id', '?basic_info:json', '?group_ids:json', '?integral_increment:json'])
    def post(args):
        corp = args['corp']
        member_id = args['id']

        #添加积分变更
        integral_increment = args.get('integral_increment', None)
        if integral_increment:
            corp.modify_member_service.add_integral(member_id, integral_increment['integral_increment'], integral_increment['reason'])

        #改变会员等级
        if 'member_grade_id' in args:
            member_grade_id = args['member_grade_id']
            corp.modify_member_service.update_grade_for_members([member_id], member_grade_id)

        if 'group_ids' in args or 'basic_info' in args:
            member = corp.member_repository.get_member_by_id(member_id)

            group_ids = args.get('group_ids', None)
            if group_ids:
                member.join_groups(group_ids)

            basic_info = args.get('basic_info', None)
            if basic_info:
                corp.modify_member_service.update_basic_member_info(member_id, basic_info)
 
        return {}