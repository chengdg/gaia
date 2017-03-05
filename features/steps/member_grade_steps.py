# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


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
            
        data['corp_id'] = context.corp.id
        response = context.client.put('/member/member_grade/', data)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获得会员等级列表")
def step_get_category(context, user):
    response = context.client.get('/member/member_grades/?corp_id=%d' % context.corp.id)
    
    actual = response.data['member_grades']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)
