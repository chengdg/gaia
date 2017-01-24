# -*- coding:utf-8 -*-

import json

from behave import *
from features.util import bdd_util

from db.mall import models as mall_models

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
			'points': data.get('points', 0.0),
			'rebate_money': data.get('rebate_money', 0.0),
			'rebate_proport': data.get('rebate_proport', 0.0),
			'default_rebate_proport': data.get('default_rebate_proport', 0.0),
			'clear_period': __format_clear_period(data['clear_period']),
			'classfication_ids': __format_classifications(data['classifications']),
			'contact': data.get('contact', ''),
			'contact_phone': data.get('contact_phone', ''),
			'service_tel': data.get('service_tel', ''),
			'service_qq_first': data.get('service_qq_first', ''),
			'service_qq_second': data.get('service_qq_second', '')
		})
	return return_data

def __format_purchase_type(purchase_type):
	return 1 if purchase_type == u'固定底价' else 2 if purchase_type == u'零售价返点' else 3

def __format_clear_period(clear_period):
	return 1 if clear_period == u'自然月' else 2 if clear_period == u'15天' else 3

def __format_classifications(classifications):
	classification_names = classifications.split(',')
	models = mall_models.Classification.select().dj_where(name__in=classification_names)

	return [m.id for m in models]