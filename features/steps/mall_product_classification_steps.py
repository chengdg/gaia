# -*- coding: utf-8 -*-
import json

from behave import *

from business.mall.corporation_factory import CorporationFactory
from features.util import bdd_util
from db.mall import models as mall_models

def __add_classification(context, classification2children, level, father_id):
	for classification in classification2children:
		data = {
			"corp_id": context.corp.id,
			"name": classification,
			"level": level,
			"father_id": father_id
		}
		response = context.client.put('/mall/product_classification/', data)
		bdd_util.assert_api_call_success(response)

		children = classification2children[classification]
		if children:
			__add_classification(context, children, level+1, response.data['id'])


@when(u"{user}添加商品分类")
def step_impl(context, user):
	classification2children = json.loads(context.text)
	level = 1
	father_id = 0
	__add_classification(context, classification2children, level, father_id)


@then(u"{user}能获取商品分类列表")
def step_impl(context, user):
	response = context.client.get('/mall/product_classifications/')

	product_classifications = response.data['product_classifications']
	father2child = dict([(classification['father_id'], classification) for classification in product_classifications])

	product_classifications.sort(lambda x,y: cmp(x['father_id'], y['father_id']))
	name2classification = dict()
	id2classification = dict()
	print (product_classifications)
	for classification in product_classifications:
		id = classification['id']
		name = classification['name']
		father_id = classification['father_id']
		if not id in id2classification:
			data = {}
			id2classification[id] = data
			if father_id == 0:
				name2classification[name] = data
		print (id2classification)
		if father_id != 0:
			id2classification[father_id][name] = id2classification[id]
	actual = name2classification

	def __change_empty_dict_to_none(a_dict):
		for key, value in a_dict.items():
			if len(value) == 0:
				a_dict[key] = None
			else:
				__change_empty_dict_to_none(a_dict[key])
	__change_empty_dict_to_none(name2classification)

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{user}删除商品分类'{classification_name}'")
def step_impl(context, user, classification_name):
	data = {
		'id': __classification_name2id(classification_name)
	}
	response = context.client.delete('/mall/product_classification/', data)
	bdd_util.assert_api_call_success(response)

def __classification_name2id(classification_name):
	return mall_models.Classification.select().dj_where(name=classification_name).get().id


@then(u"{user}能获得'{classification_name}'的子分类集合")
def step_impl(context, user, classification_name):
	classification = mall_models.Classification.select().dj_where(name=classification_name).get()

	data = {
		'corp_id': context.corp.id,
		'classification_id': classification.id
	}
	response = context.client.get('/mall/child_product_classifications/', data)

	actual = {}
	for classification in response.data['product_classifications']:
		actual[classification['name']] = True

	expected = {}
	for item in json.loads(context.text):
		expected[item] = True

	bdd_util.assert_dict(expected, actual)

@When(u"{user}为商品分类'{classification_name}'配置特殊资质")
def step_impl(context, user, classification_name):
	datas = json.loads(context.text)
	qualifications = []
	for data in datas:
		qualifications.append({
			'name': data['qualification_name']
		})

	response = context.client.put('/mall/product_classification_qualification/', {
		'classification_id': __classification_name2id(classification_name),
		'qualification_infos': json.dumps(qualifications)
	})
	bdd_util.assert_api_call_success(response)

@Then(u"{user}查看商品分类'{classification_name}'的特殊资质")
def step_impl(context, user, classification_name):
	table = context.table
	response = context.client.get('/mall/product_classifications/')
	datas = response.data['product_classifications']
	actual = []
	expected = []
	for data in datas:
		if data['name'] == classification_name:
			actual = data['qualification_infos']

	for row in table:
		expected.append({
			'name': row['qualification_name']
		})

	bdd_util.assert_list(expected, actual)

@When(u"{user}删除商品分类'{classification_name}'中已经分配的资质")
def step_impl(context, user, classification_name):
	datas = json.loads(context.text)
	#获得该商品分类的所有资质
	classification_id = __classification_name2id(classification_name)
	weizoom_corp = CorporationFactory.get_weizoom_corporation()
	classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
	all_qualifications = classification.get_qualifications()
	#去除将要删除的资质
	for data in datas:
		name = data['qualification_name']
		for qualification in all_qualifications:
			if qualification.name == name:
				all_qualifications.remove(qualification)

	response = context.client.put('/mall/product_classification_qualification/', {
		'classification_id': classification_id,
		'qualification_infos': json.dumps([{'id': q.id, 'name': q.name} for q in all_qualifications])
	})

	bdd_util.assert_api_call_success(response)

@when(u"{user}为商品分类'{classification_name}'配置标签")
def step_impl(context, user, classification_name):
	datas = json.loads(context.text)
	selected_labels = []
	classification_id = __classification_name2id(classification_name)
	for data in datas:
		selected_labels.append({
			'labelGroupId': label_group_name2id(data['label_group_name']),
			'labelIds': map(lambda x: label_name2id(x), data['labels'])
		})

	print (selected_labels)

	response = context.client.put('/mall/product_classification_label/', {
		'classification_id': classification_id,
		'selected_labels': json.dumps(selected_labels)
	})
	bdd_util.assert_api_call_success(response)

@then(u"{user}查看商品分类列表")
def step_impl(context, user):
	expected = bdd_util.table2list(context)
	for one in expected:
		one['operation'] = one['operation'].split(',')
	actual = __view_classification_list(context)
	print (expected)
	print (actual)
	bdd_util.assert_list(expected, actual)

@then(u"{user}查看商品分类'{classification_name}'的二级分类")
def step_impl(context, user, classification_name):
	classification_id = __classification_name2id(classification_name)
	expected = bdd_util.table2list(context)
	for one in expected:
		print (isinstance(one['operation'], unicode))
		one['operation'] = one['operation'].split(',')
	actual = __view_classification_list(context, classification_id)
	print (expected)
	print (actual)
	bdd_util.assert_list(expected, actual)

@then(u"{user}查看商品分类'{classification_name}'的标签")
def step_impl(context, user, classification_name):
	expected = json.loads(context.text)
	classification_id = __classification_name2id(classification_name)
	response = context.client.get('/mall/product_classification_label/', {
		'classification_id': classification_id
	})
	resp_datas = response.data
	actual = []
	for data in resp_datas:
		label_group_name = label_group_id2name(data['labelGroupId'])
		label_ids = map(lambda x: label_id2name(x), data['labelIds'])
		actual.append({
			'label_group_name': label_group_name,
			'labels': label_ids
		})

	print (expected)
	print (actual)
	bdd_util.assert_list(expected, actual)


def __view_classification_list(context, father_id=0):


	data = {
		'father_id': father_id
	}

	response = context.client.get('/mall/product_classifications/', data)
	data_list = response.data['product_classifications']
	use_data_list = []

	for one in data_list:
		use_data = dict()
		use_data['classfication_name'] = one['name']

		operation_list = [u'修改', u'删除']
		if father_id != 0:
			operation_list.append(u'配置特殊资质')

		if one['has_label']:
			operation_list.append(u'已配置标签')
		else:
			operation_list.append(u'配置标签')
		use_data['operation'] = operation_list
		use_data_list.append(use_data)

	return use_data_list


def label_group_name2id(label_group_name):
	label_group = mall_models.ProductLabelGroup.select().dj_where(name=label_group_name).get()
	return label_group.id

def label_group_id2name(label_group_id):
	label_group = mall_models.ProductLabelGroup.select().dj_where(id=label_group_id).get()
	return label_group.name

def label_name2id(label_name):
	label = mall_models.ProductLabel.select().dj_where(name=label_name).get()
	return label.id

def label_id2name(label_id):
	label = mall_models.ProductLabel.select().dj_where(id=label_id).get()
	return label.name