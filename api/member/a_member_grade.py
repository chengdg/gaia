# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.member_grade import MemberGrade
from business.member.member import Member


class AMemberGrade(api_resource.ApiResource):
    """
    会员等级
    """
    app = "member"
    resource = "member_grade"

    @param_required(['corp_id', 'name', 'is_auto_upgrade:bool', 'shop_discount'])
    def put(args):
        member_grade = MemberGrade.create(args)
        
        return {
            'id': member_grade.id
        }

    @param_required(['corp_id', 'id'])
    def get(args):
        corp = args['corp']
        member_grade = corp.member_grade_repository.get_member_grade_by_id(args['id'])
        
        return {
            'id': member_grade.id,
            'name': member_grade.name,
            'is_default_grade': member_grade.is_default_grade,
            'is_auto_upgrade': member_grade.is_auto_upgrade,
            'pay_money': member_grade.pay_money,
            'pay_times': member_grade.pay_times,
            'shop_discount': member_grade.shop_discount
        }
