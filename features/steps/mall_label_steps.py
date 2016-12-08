# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models


@when(u"{user}新增商品标签分组")
def step_impl(context, user):
	label_groups_data = json.loads(context.text)
	if isinstance(label_groups_data, list):
		for label_group_dict in label_groups_data:
			label_group_name = label_group_dict['label_group_name']
			__add_product_label_group(context, label_group_name)
	else:
		__add_product_label_group(context, label_groups_data['label_group_name'])

@then(u"{user}查看商品标签列表")
def step_impl(context, user):
	expected = bdd_util.table2dict(context)
	response = context.client.get('/mall/product_label_groups/')
	actual = response.data['product_label_groups']
	for data in expected:
		if data['labels'] == '':
			data['labels'] = []
	bdd_util.assert_list(expected, actual)

@when(u"{user}删除商品标签分组")
def step_impl(context, user):
	label_groups_data = json.loads(context.text)
	if isinstance(label_groups_data, list):
		for label_group_dict in label_groups_data:
			label_group_name = label_group_dict['label_group_name']
			__del_product_label_group(context, label_group_name)
	else:
		__del_product_label_group(context, label_groups_data['label_group_name'])

def __add_product_label_group(context, label_group_name):
	response = context.client.put('/mall/product_label_group/', {
		'label_group_name': label_group_name
	})
	bdd_util.assert_api_call_success(response)

def __del_product_label_group(context, label_group_name):
	label_group_id = label_group_name2id(label_group_name)
	response = context.client.delete('/mall/product_label_group/', {
		'label_group_id': label_group_id
	})
	bdd_util.assert_api_call_success(response)

def label_group_name2id(label_group_name):
	label_group = mall_models.ProductLabelGroup.select().dj_where(name=label_group_name).get()
	return label_group.id