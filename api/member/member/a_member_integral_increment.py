# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member import Member

class AMemberIntegralIncrement(api_resource.ApiResource):
    """
    会员积分增量
    """
    app = "member"
    resource = "integral_increment"

    @param_required(['corp_id', 'member_id', 'integral_increment:int', 'reason'])
    def put(args):
        corp = args['corp']
        corp.modify_member_service.add_integral(args['member_id'], args['integral_increment'], args['reason'])
        
        return {}
