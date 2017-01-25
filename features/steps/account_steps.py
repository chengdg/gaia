# -*- coding:utf-8 -*-

import json

from behave import *
from features.util import bdd_util

from db.mall import models as mall_models

@when(u"{user}配置'{corp_name}'的账号信息")
def step_impl(context, user, corp_name):
	data = json.loads(context.text)
	req_data = __format_request_data(data)
	req_data['corp_id'] = bdd_util.get_user_id_for(corp_name)
	response = context.client.post('/account/corp/', req_data)
	bdd_util.assert_api_call_success(response)

@then(u"{user}能获取账号配置列表")
def step_impl(context, user):
	expected = bdd_util.table2list(context)
	response = context.client.get('/account/corps/', {})

	expected_corp_names = [e['name'] for e in expected]

	actual = response.data['rows']

	new_rows = []

	for row in actual:
		if row['name'] not in expected_corp_names:
			continue
		row['classifications'] = __classification_ids2names(row['classification_ids'])
		row['customer_from'] = u'渠道'
		row['created_time'] = u'创建时间'
		row['operation'] = u'编辑'
		row['purchase_type'] = __purchase_type_num2str(row['purchase_method'])
		row['clear_period'] = __clear_period_num2str(row['clear_period'])

		new_rows.append(row)

	bdd_util.assert_list(expected, new_rows)

def __classification_ids2names(ids):
	ids = ids.split(',')
	models = mall_models.Classification.select().dj_where(id__in=ids)
	return ','.join([m.name for m in models])

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
			'max_product_count': data['max_product_count'],
			'points': data.get('points', 0.0),
			'rebate_money': data.get('rebate_money', 0.0),
			'rebate_proport': data.get('rebate_proport', 0.0),
			'default_rebate_proport': data.get('default_rebate_proport', 0.0),
			'clear_period': __format_clear_period(data['clear_period']),
			'classification_ids': __format_classifications(data['classifications']),
			'contact': data.get('contact', ''),
			'contact_phone': data.get('contact_phone', ''),
			'service_tel': data.get('service_tel', ''),
			'service_qq_first': data.get('service_qq_first', ''),
			'service_qq_second': data.get('service_qq_second', '')
		})
	return return_data

def __format_purchase_type(purchase_type):
	return 1 if purchase_type == u'固定底价' else 2 if purchase_type == u'零售价返点' else 3

def __purchase_type_num2str(num):
	return u'固定底价' if num == 1 else u'零售价返点' if num == 2 else u'首月分成'

def __format_clear_period(clear_period):
	return 1 if clear_period == u'自然月' else 2 if clear_period == u'15天' else 3

def __clear_period_num2str(num):
	return u'自然月' if num == 1 else u'15天' if num == 2 else u'自然周'

def __format_classifications(classifications):
	models = mall_models.Classification.select().dj_where(name__in=classifications)

	return ','.join([str(m.id) for m in models])