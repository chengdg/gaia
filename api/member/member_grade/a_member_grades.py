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

    @param_required(['corp_id', '?with_member_count:bool'])
    def get(args):
        corp = args['corp']
        member_grades = corp.member_grade_repository.get_member_grades()

        with_member_count = args.get('with_member_count', False)

        datas = []
        for member_grade in member_grades:
            datas.append({
                'id': member_grade.id,
                'name': member_grade.name,
                'is_default_grade': member_grade.is_default_grade,
                'is_auto_upgrade': member_grade.is_auto_upgrade,
                'pay_money': member_grade.pay_money,
                'pay_times': member_grade.pay_times,
                'shop_discount': member_grade.shop_discount,
                'upgrade_strategy': corp.member_grade_repository.get_upgrade_strategy(),
                'member_count': member_grade.member_count if with_member_count else 0
            })
        
        return {
            'member_grades': datas
        }
