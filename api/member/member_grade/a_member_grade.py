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

    @param_required(['corp_id', 'name', 'is_auto_upgrade:bool', 'shop_discount', 'pay_money', 'pay_times'])
    def put(args):
        member_grade = MemberGrade.create(args)
        
        return {
            'id': member_grade.id
        }

    @param_required(['corp_id', 'id', 'name', 'is_auto_upgrade:bool', 'shop_discount', 'pay_money', 'pay_times'])
    def post(args):
        corp = args['corp']
        member_grade = corp.member_grade_repository.get_member_grade_by_id(args['id'])
        member_grade.update({
            'name': args['name'],
            'is_auto_upgrade': args['is_auto_upgrade'],
            'pay_money': args['pay_money'],
            'pay_times': args['pay_times'],
            'shop_discount': args['shop_discount']
        })
        
        return {}

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
            'shop_discount': member_grade.shop_discount,
            'upgrade_strategy': corp.member_grade_repository.get_upgrade_strategy()
        }

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        corp.member_grade_repository.delete_member_grade(args['id'])
        
        return {}
