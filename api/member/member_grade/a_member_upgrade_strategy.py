# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member_grade import MemberGrade
from business.member.member import Member


class AMemberUpgradeStrategy(api_resource.ApiResource):
    """
    会员等级的升级策略
    """
    app = "member"
    resource = "member_upgrade_strategy"

    @param_required(['corp_id'])
    def get(args):
        corp = args['corp']
        strategy = corp.member_grade_repository.get_upgrade_strategy()
        
        return {
            'strategy': strategy
        }

    @param_required(['corp_id', 'strategy'])
    def post(args):
        corp = args['corp']
        corp.member_grade_repository.modify_upgrade_strategy(args['strategy'])
        
        return {}
