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

        return {
            'id': member.id,
            'name': member.username
        }