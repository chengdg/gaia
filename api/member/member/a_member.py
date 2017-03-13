# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member


class AMember(api_resource.ApiResource):
    """
    会员
    """
    app = "member"
    resource = "member"

    @param_required(['corp_id', 'id'])
    def get(args):
        corp = args['corp']
        member = corp.member_repository.get_member_by_id(args['id'])

        member_grade = member.grade

        group_datas = []
        for member_tag in member.tags:
            group_datas.append({
                'id': member_tag.id,
                'name': member_tag.name
            })

        data = {
            'id': member.id,
            'name': member.username,
            'grade': {
                'id': member_grade.id,
                'name': member_grade.name
            },
            'groups': group_datas
        }

        return data