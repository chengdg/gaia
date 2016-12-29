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
			__add_product_label_group(context, user, label_group_name)
	else:
		__add_product_label_group(context, user, label_groups_data['label_group_name'])

@then(u"{user}查看商品标签列表")
def step_impl(context, user):
	expected = bdd_util.table2list(context)
	response = context.client.get('/mall/product_label_groups/', {
		'corp_id': bdd_util.get_user_id_for(user)
	})
	actual = response.data['product_label_groups']
	for data in expected:
		tmp_list = []
		if data['labels'] == '':
			data['labels'] = tmp_list
		else:
			for label in data['labels'].split(','):
				tmp_list.append({
					'label_name': label
				})
			data['labels'] = tmp_list
	bdd_util.assert_list(expected, actual)

@when(u"{user}删除商品标签分组")
def step_impl(context, user):
	label_groups_data = json.loads(context.text)
	if isinstance(label_groups_data, list):
		for label_group_dict in label_groups_data:
			label_group_name = label_group_dict['label_group_name']
			__del_product_label_group(context, user, label_group_name)
	else:
		__del_product_label_group(context, user, label_groups_data['label_group_name'])

@when(u"{user}添加商品标签")
def step_impl(context, user):
	labels_data = json.loads(context.text)
	if isinstance(labels_data, list):
		for label_group_dict in labels_data:
			label_group_name = label_group_dict['label_group_name']
			label_name_list = label_group_dict['labels']
			for label_name in label_name_list:
				__add_product_label(context, user, label_group_name, label_name)
	else:
		label_name_list = labels_data['labels']
		for label_name in label_name_list:
			__add_product_label(context, user, labels_data['label_group_name'], label_name)

@when(u"{user}删除商品标签")
def step_impl(context, user):
	labels_data = json.loads(context.text)
	if isinstance(labels_data, list):
		for label_group_dict in labels_data:
			label_name = label_group_dict['label_name']
			__del_product_label(context, user, label_name)
	else:
		__del_product_label(context, user, labels_data['label_name'])

def __del_product_label(context, user, label_name):
	label_id = label_name2id(label_name)
	response = context.client.delete('/mall/product_label/', {
		'corp_id': bdd_util.get_user_id_for(user),
		'label_id': label_id,
	})
	bdd_util.assert_api_call_success(response)

def __add_product_label(context, user, label_group_name, label_name):
	label_group_id = label_group_name2id(label_group_name)
	response = context.client.put('/mall/product_label/', {
		'corp_id': bdd_util.get_user_id_for(user),
		'label_group_id': label_group_id,
		'label_name': label_name
	})
	bdd_util.assert_api_call_success(response)

def __add_product_label_group(context, user, label_group_name):
	response = context.client.put('/mall/product_label_group/', {
		'corp_id': bdd_util.get_user_id_for(user),
		'label_group_name': label_group_name
	})
	bdd_util.assert_api_call_success(response)

def __del_product_label_group(context, user, label_group_name):
	label_group_id = label_group_name2id(label_group_name)
	response = context.client.delete('/mall/product_label_group/', {
		'corp_id': bdd_util.get_user_id_for(user),
		'label_group_id': label_group_id
	})
	bdd_util.assert_api_call_success(response)

def label_group_name2id(label_group_name):
	label_group = mall_models.ProductLabelGroup.select().dj_where(name=label_group_name).get()
	return label_group.id

def label_name2id(label_name):
	label = mall_models.ProductLabel.select().dj_where(name=label_name).get()
	return label.id