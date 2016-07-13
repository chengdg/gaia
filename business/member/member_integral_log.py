# -*- coding: utf-8 -*-
# author : rocky

from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.cache import utils as cache_util

from business import model as business_model

from db.member import models as member_models


class MemberIntegralLog(business_model.Model):
    '''
    会员积分log
    '''
    __slots__ = (
        'id',
        'webapp_user_id',
        'event_type',
        'integral_count',
        'reason',
        'current_integral',
        'manager',
        'created_at'
    )
    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def empty_member_integrallog(medel=None):
        return MemberIntegralLog(medel)

    @property
    def member(self):
        pass

    def create(self, member, event_type, integral_count, reason, manager, current_integral):
        opt = {
            'member': member.get_db_model,
            # 'webapp_user_id': webapp_user_id,
            'event_type': event_type,
            'integral_count': integral_count,
            'reason': reason,
            'manager': manager,
            'current_integral': current_integral
        }
        mem_integral_log = member_models.MemberIntegralLog.create(**opt)
        return MemberIntegralLog(mem_integral_log)
