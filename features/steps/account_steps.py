# -*- coding:utf-8 -*-

import json

from behave import *
from features.util import bdd_util

@when(u"{user}配置'{corp_name}'的账号信息")
def step_impl(context, user, corp_name):
	data = json.loads(context.text)
	req_data = __format_request_data(data)
	response = context.client.post('/account/corp/', req_data)
	bdd_util.assert_api_call_success(response)


def __format_request_data(data):
	is_weizoom_corp = True if data['account_type'] == u'运营' else False
	return_data = {
		'is_weizoom_corp': is_weizoom_corp,
		'name': data['name'],
		'note': data['note']
	}
	if not is_weizoom_corp:
		return_data.update({
			'company_name': data['company_name'],
			'purchase_method': __format_purchase_type(data['purchase_type']),
			'points': data['points'],

		})

def __format_purchase_type(purchase_type):
	return 1 if purchase_type == u'固定底价' else 2 if purchase_type == u'零售价返点' else 3