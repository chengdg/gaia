# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.member.member_integral_log import MemberIntegralLog
from business.member.member_integral_log_factory import MemberIntegralLogFactory
from business.member.member import Member
from db.member import models as member_models

class AMemberIntegralLog(api_resource.ApiResource):
    """
    会员积分log
    """
    app = 'member'
    resource = 'member_integral_log'    

    @param_required(['member_id', 'integral'])
    def  post(args):
        member = Member.from_id({'id': args['member_id']})
        if not member:
            return {}
        try:
            integral = int(args['integral'])
        except ValueError:
            return {'msg': u'{} invalid int type'.format(args['integral'])}
        event_type = None
        if integral  < 0:
            event_type = member_models.MANAGER_MODIFY_REDUCT
        # 积分日志
        # @@@@工厂类
        # import pdb
        # pdb.set_trace()
        member_integral_log = MemberIntegralLogFactory.save({
            'member': member,
            'integral_count': integral,
            'manager': member.member_webapp_manager.username,
            'current_integral': member.integral ,
            'reason': args['reason'] if args.get('reason', None) else '',
            'event_type': event_type
        })
        return {
            'integral': member_integral_log.current_integral
        }