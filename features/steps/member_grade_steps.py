# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models
from db.member import models as member_models


@when(u"{user}创建会员等级")
def step_impl(context, user):
    member_grades = json.loads(context.text)
    if type(member_grades) == dict:
        member_grades = [member_grades]

    for member_grade in member_grades:
        data = member_grade
        if not 'is_auto_upgrade' in data:
            data['is_auto_upgrade'] = False
        if not 'shop_discount' in data:
            data['shop_discount'] = 10
        if not 'pay_money' in data:
            data['pay_money'] = 0.0
        if not 'pay_times' in data:
            data['pay_times'] = 0
            
        data['corp_id'] = context.corp.id
        response = context.client.put('/member/member_grade/', data)
        bdd_util.assert_api_call_success(response)

@when(u"{user}更新会员等级'{member_grade_name}'为")
def step_impl(context, user, member_grade_name):
    target_member_grade = member_models.MemberGrade.select().dj_where(name=member_grade_name).get()

    data = json.loads(context.text)
    if not 'is_auto_upgrade' in data:
        data['is_auto_upgrade'] = False
    if not 'shop_discount' in data:
        data['shop_discount'] = 10
    if not 'pay_money' in data:
        data['pay_money'] = 0.0
    if not 'pay_times' in data:
        data['pay_times'] = 0
            
    data['corp_id'] = context.corp.id
    data['id'] = target_member_grade.id
    response = context.client.post('/member/member_grade/', data)
    bdd_util.assert_api_call_success(response)

@when(u"{user}更新会员升级策略为'{upgrade_strategy}'")
def step_impl(context, user, upgrade_strategy):
    if upgrade_strategy == u'满足全部条件':
        upgrade_strategy = 'match_all'
    elif upgrade_strategy == u'满足任一条件':
        upgrade_strategy = 'match_any'

    data = {
        'corp_id': context.corp.id,
        'strategy': upgrade_strategy
    }
            
    response = context.client.post('/member/member_upgrade_strategy/', data)
    bdd_util.assert_api_call_success(response)

@then(u"{user}能获得会员升级策略为'{expected_strategy}'")
def step_impl(context, user, expected_strategy):
    url = '/member/member_upgrade_strategy/?corp_id=%s' % context.corp.id
    response = context.client.get(url)

    strategy = response.data['strategy']
    if strategy == 'match_all':
        actual = u'满足全部条件'
    elif strategy == 'match_any':
        actual = u'满足任一条件'

    expected = expected_strategy
    context.tc.assertEqual(expected, actual)


@when(u"{user}删除会员等级'{member_grade_name}'")
def step_impl(context, user, member_grade_name):
    target_member_grade = member_models.MemberGrade.select().dj_where(name=member_grade_name).get()
    data = {}        
    data['corp_id'] = context.corp.id
    data['id'] = target_member_grade.id

    response = context.client.delete('/member/member_grade/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得会员等级列表")
def step_get_category(context, user):
    response = context.client.get('/member/member_grades/?corp_id=%d' % context.corp.id)
    
    actual = response.data['member_grades']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)
