# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.member.member import Member


class AMemberIntegral(api_resource.ApiResource):
    """
    会员积分
    """
    app = 'member'
    resource = 'member_integral'

    @param_required(['member_id'])
    def get(args):
        '''
        会员积分
        '''
        return {}

    @param_required(['member_id', 'integral'])
    def put(args):
        '''
        修改会员积分
        '''
        member = Member.from_id({'id': args['member_id']})
        if not member:
            return {}
        try:
            integral = int(args['integral'])
        except ValueError:
            return {'msg': u'{} invalid int type'.format(args['integral'])}
        count = member.update_member_integral(args['member_id'], integral)
        return {
            'count': count
        }

