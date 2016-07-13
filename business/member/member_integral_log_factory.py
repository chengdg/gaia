# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model

from business.member.member_integral_log import MemberIntegralLog
from db.member import models as member_models

class MemberIntegralLogFactory(business_model.Model):
    '''
    member integral log 工厂类
    '''

    __slots__ = (
    )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    @param_required(['member', 'integral_count', 'manager', 'current_integral'])
    def  save(args):
        member_integral_log = MemberIntegralLog.empty_member_integrallog()
        event_type = args['event_type'] if args.get('event_type', None) else member_models.MANAGER_MODIFY_ADD
        reason = args['reason'] if args.get('reason', None) else ''
        return member_integral_log.create(args['member'], event_type, args['integral_count'], reason, args['manager'], args['current_integral'])