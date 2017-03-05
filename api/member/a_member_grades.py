# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.social_account import SocialAccount
from business.member.member import Member


class AMemberGrades(api_resource.ApiResource):
    """
    会员等级集合
    """
    app = "member"
    resource = "member_grades"

    @param_required(['corp_id'])
    def get(args):
        corp = args['corp']
        member_grades = corp.member_grade_repository.get_member_grades()

        datas = []
        for member_grade in member_grades:
            datas.append({
                'id': member_grade.id,
                'name': member_grade.name,
                'is_default_grade': member_grade.is_default_grade,
                'is_auto_upgrade': member_grade.is_auto_upgrade,
                'pay_money': member_grade.pay_money,
                'pay_times': member_grade.pay_times,
                'shop_discount': member_grade.shop_discount
            })
        
        return {
            'member_grades': datas
        }
