# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models


def __limit_type_name2number(name):
	if u'无限制' == name:
		return 0
	elif u'仅发货地区' == name:
		return 1
	elif u'不发货地区' == name:
		return 2
	else:
		return -1

def __postage_type_name2bool(name):
	if u"统一运费" == name:
		return True
	else:
		return False

def __product_names2ids_str(name_list):
	models = mall_models.Product.select().dj_where(name__in=name_list, is_pre_product=True)
	return [m.id for m in models]

def __classification_name2id(classification_name):
	return mall_models.Classification.select().dj_where(name=classification_name).get().id

def __get_operations(context, status):
	#运营
	operations = []
	if bdd_util.is_weizoom_corp(context.corp.id):
		if status == mall_models.PRODUCT_PENDING_STATUS['SUBMIT']:
			operations.append(u'通过')
			operations.append(u'驳回')
		operations.append(u'删除')
	else:
		operations.append(u'编辑')

	return ' '.join(operations)

@when(u"{user}创建商品分类为'{classification_name}'的待审核商品")
def step_impl(context, user, classification_name):
	datas = json.loads(context.text)
	classification_id = __classification_name2id(classification_name)
	for data in datas:
		response = context.client.put('/mall/pre_product/', {
			'corp_id': bdd_util.get_user_id_for(user),
			'classification_id': classification_id,
			'name': data['name'],
			'promotion_title': data['promotion_title'],
			'has_multi_models': data['has_product_model'],
			'price': data['price'],
			'weight': data['weight'],
			'stocks': data['stock'],
			'limit_zone_type': __limit_type_name2number(data['limit_zone_type']),
			'has_same_postage': __postage_type_name2bool(data['postage_type']),
			'postage_money': data['postage_money'],
			'detail': data['remark']
		})
		bdd_util.assert_api_call_success(response)

@when(u"{user}审核通过待审核商品")
def step_impl(context, user):
	datas = json.loads(context.text)
	response = context.client.put('/mall/pending_product/', {
		'corp_id': bdd_util.get_user_id_for(user),
		'product_ids': json.dumps(__product_names2ids_str(datas))
	})
	bdd_util.assert_api_call_success(response)

@then(u"{user}查看待审核商品列表")
def step_impl(context, user):
	expected = bdd_util.table2list(context)
	response = context.client.get('/mall/pre_products/', {
		'corp_id': bdd_util.get_user_id_for(user)
	})

	actual = response.data['rows']

	for row in actual:
		row['classfication'] = row['classification_name_nav']
		row['created_time'] = u'创建时间'
		row['operation'] = __get_operations(context, row['status'])
		row['status'] = row['status_text']
		row['stock'] = row['stocks']

	bdd_util.assert_list(expected, actual)


