# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@when(u"{user}更新积分规则为")
def step_impl(context, user):
    data = json.loads(context.text)
    data['corp_id'] = context.corp.id

    response = context.client.post('/mall/integral_strategy/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得积分规则")
def step_impl(context, user):
    data = {
        "corp_id": context.corp.id
    }
    response = context.client.get('/mall/integral_strategy/', data)
    actual = response.data

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}更新Webapp配置为")
def step_impl(context, user):
    data = json.loads(context.text)
    for key, value in data.items():
        if value == True:
            data[key] = 'true'
        if value == False:
            data[key] = 'false'
    data['corp_id'] = context.corp.id

    response = context.client.post('/mall/webapp_config/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得Webapp配置")
def step_impl(context, user):
    data = {
        "corp_id": context.corp.id
    }
    response = context.client.get('/mall/webapp_config/', data)
    actual = response.data

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)
