# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@when(u"{user}更新积分规则为")
def step_impl(context, user):
	data = json.loads(context.text)
	req_data = {
		"integral_each_yuan": data.get('integral_each_yuan', 0),
		"be_member_increase_count": data.get('be_member_increase_count', 0),
		"click_shared_url_increase_count": data.get('click_shared_url_increase_count', 0),
		"buy_award_count_for_buyer": data.get('buy_award_count_for_buyer', 0),
		"order_money_percentage_for_each_buy": data.get('order_money_percentage_for_each_buy', 0),
		"buy_via_shared_url_increase_count_for_author": data.get('buy_via_shared_url_increase_count_for_author', 0),
		"buy_via_offline_increase_count_for_author": data.get('buy_via_offline_increase_count_for_author', 0),
		"buy_via_offline_increase_count_percentage_for_author": data.get(
			'buy_via_offline_increase_count_percentage_for_author', 0),
		"use_ceiling": data.get('use_ceiling', 0),
		"review_increase": data.get('review_increase', 0)
	}
	req_data['corp_id'] = context.corp.id
	response = context.client.post('/mall/integral_strategy/', req_data)
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
