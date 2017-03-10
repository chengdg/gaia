# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models
from db.member import models as member_models


@when(u"{user}创建会员分组")
def step_impl(context, user):
    member_groups = json.loads(context.text)
    if type(member_groups) == dict:
        member_groups = [member_groups]

    for member_group in member_groups:
        data = member_group    
        data['corp_id'] = context.corp.id
        response = context.client.put('/member/member_group/', data)
        bdd_util.assert_api_call_success(response)

@when(u"{user}更新会员分组'{member_group_name}'为")
def step_impl(context, user, member_group_name):
    target_member_group = member_models.MemberTag.select().dj_where(name=member_group_name).get()

    data = json.loads(context.text)
    data['corp_id'] = context.corp.id
    data['id'] = target_member_group.id
    response = context.client.post('/member/member_group/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除会员分组'{member_group_name}'")
def step_impl(context, user, member_group_name):
    target_member_group = member_models.MemberTag.select().dj_where(name=member_group_name).get()
    data = {}        
    data['corp_id'] = context.corp.id
    data['id'] = target_member_group.id

    response = context.client.delete('/member/member_group/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得会员分组列表")
def step_get_category(context, user):
    response = context.client.get('/member/member_groups/?corp_id=%d&with_member_count=true' % context.corp.id)
    
    actual = response.data['member_groups']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)
