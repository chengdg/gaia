# -*- coding: utf-8 -*-
import json

from behave import *

from business.mall.corporation_factory import CorporationFactory
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

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