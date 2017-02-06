# -*- coding: utf-8 -*-
import HTMLParser
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
def __limit_type_number2name(num):
	num = int(num)
	if num == 0:
		return u'无限制'
	elif num == 1:
		return u'仅发货地区'
	elif num == 2:
		return u'不发货地区'
	else:
		return ''

def __limit_zone_name2id(name, corp_id):
	if not name:
		return 0
	return mall_models.ProductLimitZoneTemplate.select().dj_where(owner_id=corp_id, name=name).get().id

def __limit_zone_id2name(id, corp_id):
	if int(id) == 0:
		return ''
	else:
		return mall_models.ProductLimitZoneTemplate.select().dj_where(owner_id=corp_id, id=id).get().name

def __get_product_owner_id(product_id):
	return mall_models.Product.select().dj_where(id=product_id).get().owner_id

def __get_product_status_text(status, is_accepted):
	"""
	:return: 待审核, 审核中, 已审核, 入库驳回
	"""
	PRODUCT_STATUS = {
		'NOT_YET': 0, #尚未提交审核
		'SUBMIT': 1, #提交审核
		'REFUSED': 2 #驳回
	}
	status_text = u'待审核'

	if is_accepted:
		status_text = u'已审核'

	if status == PRODUCT_STATUS['REFUSED'] and not is_accepted:
		status_text = u'入库驳回'
	elif status == PRODUCT_STATUS['REFUSED'] and is_accepted:
		status_text = u'修改驳回'

	if status == PRODUCT_STATUS['SUBMIT']:
		status_text = u'审核中'

	return status_text

def __postage_type_name2bool(name):
	if u"统一运费" == name:
		return True
	else:
		return False

def __postage_name2id(name, corp_id):
	if u"统一运费" == name:
		return 0
	else:
		postage_name = name.split(':')[1]
		return mall_models.PostageConfig.select().dj_where(owner_id=corp_id, is_deleted=False, is_used=True, name=postage_name).get().id

def __postage_id2name(id, corp_id):
	if int(id) == 0:
		return u'统一运费'
	else:
		name = mall_models.PostageConfig.select().dj_where(owner_id=corp_id, is_deleted=False, is_used=True, id=id).get().name
		return u'使用默认运费模板:{}'.format(name)

def __product_names2ids_str(name_list):
	models = mall_models.Product.select().dj_where(name__in=name_list, is_pre_product=True)
	return [m.id for m in models]

def __classification_name2id(classification_name, product_name):
	if not classification_name:
		product_id = mall_models.Product.select().dj_where(name=product_name, is_pre_product=True).get().id
		return mall_models.ClassificationHasProduct.select().dj_where(product_id=product_id).get().classification_id

	return mall_models.Classification.select().dj_where(name=classification_name).get().id

def __get_operations(context, status, is_accepted):
	#运营
	operations = []
	if bdd_util.is_weizoom_corp(context.corp.id):
		if status == mall_models.PRODUCT_STATUS['SUBMIT']:
			operations.append(u'通过')
			operations.append(u'驳回')
		if not is_accepted:
			operations.append(u'删除')
	else:
		operations.append(u'编辑')

	return ' '.join(operations)

def __format_image_info(images):
	return [{
			"url": image,
			"width": 80,
			"height": 80
		}for image in images]

def __format_resp_image_info(images):
	result = []
	for image in images:
		result.append(image['url'])

	return result

def __format_product_models(context, models):
	result_models = []
	if len(models) == 0:
		return result_models
	for name, model in models.items():
		data = {
			'price': model['price'],
			'weight': model['weight'],
			'stocks': model['stocks']
		}
		normalized_model_name, model_properties = __parse_model_name(context, name)
		data['name'] = normalized_model_name
		data['properties'] = model_properties

		# 在数据库中查询是否已存在该model，如果存在，则是更新；否则，为创建
		try:
			existed_product_model = mall_models.ProductModel.select().dj_where(owner_id=context.corp.id, name=normalized_model_name, is_deleted=False).get()
		except:
			existed_product_model = None
		if existed_product_model:
			data['id'] = existed_product_model.id
		else:
			data['id'] = normalized_model_name

		result_models.append(data)

	return result_models

def __format_resp_models_info(models):
	"""
	两种情况
	"""
	model_property_value_id2name = {v.id: v.name for v in mall_models.ProductModelPropertyValue.select()}
	result = dict()

	for model in models:
		if model.get('properties'):
			property_value_ids = [p['property_value_id'] for p in model['properties']]
			title = []
			for value_id in property_value_ids:
				title.append(model_property_value_id2name[value_id])

		else:
			property_value_ids = []
			title = []
			for property in model['property_values']:
				property_value_ids.append(property['id'])
				title.append(property['name'])

		title = ' '.join(title)
		result[title] = {
			"price": model['price'],
			"weight": model['weight'],
			"stocks": model['stocks']
		}
	return result


def __parse_model_name(context, model_name):
    """
    解析model name（黑色 M），生成
    1. 标准model_name: 2:5_3:6
    2. model properties: [{property_id:2, property_value_id:5}, {property_id:3, property_value_id:6}]
    """
    properties = list(mall_models.ProductModelProperty.select().dj_where(owner_id=context.corp.id))
    property_ids = [property.id for property in properties]
    property_values = list(mall_models.ProductModelPropertyValue.select().dj_where(property_id__in=property_ids))

    name2value = {}
    for property_value in property_values:
        name = property_value.name
        name2value[name] = property_value

    #从显示用的model_name(黑色 M)构造标准model_name(2:5_3:6)
    normalized_model_name_items = []
    #从model_name(黑色 M)获得model properties
    model_properties = []
    for property_value_name in model_name.split(' '):
        #property_value_name: '黒'' 或是 'M'
        property_value = name2value[property_value_name]
        normalized_model_name_item = '%d:%d' % (property_value.property_id, property_value.id)
        normalized_model_name_items.append(normalized_model_name_item)
        model_properties.append({
            'property_id': property_value.property_id,
            'property_value_id': property_value.id
        })
    normalized_model_name = '_'.join(normalized_model_name_items)

    return normalized_model_name, model_properties

def __format_price(price):
	"""
	两位小数，不足补0
	"""
	price = str(price)
	str_arr = price.split('.')
	if len(str_arr) == 1:
		return '{}.00'.format(price)
	elif len(str_arr[1]) == 1:
		return '{}0'.format(price)
	else:
		return price

def __get_stocks_area(stocks):
	if len(stocks) == 1:
		result = str(stocks[0])
	else:
		result = u'{}~{}'.format(stocks[0], stocks[-1])
	return result

def __format_price_area(price_info):
	min_price = price_info['min_price']
	max_price = price_info['max_price']
	if min_price == max_price:
		return min_price
	else:
		return '{}~{}'.format(__format_price(min_price), __format_price(max_price))

def __format_post_data(context, post):
	corp_id = context.corp.id
	custom_models = __format_product_models(context, post.get('models', []))

	has_multi_models = post.get('has_product_model', False)
	price = post.get('price', 0.0)
	purchase_price = post.get('purchase_price', 0.0)
	weight = post.get('weight', 0)
	stocks = post.get('stock', 0)
	images = __format_image_info(post.get('images', []))
	classification_id = __classification_name2id(post.get('classification', ''), post['name'])

	parser = HTMLParser.HTMLParser()

	base_info = {
		'name': post['name'],
		'promotion_title': post.get('promotion_title', ''),
		'detail': parser.unescape(post.get('remark', '')),
		'price': price,
		'purchase_price': purchase_price,
		'classification_id': classification_id,
		'is_pre_product': True
	}

	image_info = {'images': images}

	postage_info = {
		'postage_type': __postage_type_name2bool(post['postage_type']),
		'postage_id': __postage_name2id(post.get('postage_type', 0), corp_id),
		'unified_postage_money': post.get('postage_money', 0),
		'limit_zone_type': __limit_type_name2number(post['limit_zone_type']),
		'limit_zone_id': __limit_zone_name2id(post.get('limit_zone_name', ''), corp_id)
	}

	models_info = {
		'is_use_custom_model': has_multi_models,
		'standard_model': {
			'price': price,
			'purchase_price': purchase_price,
			'weight': weight,
			'stocks': stocks,
			'stock_type': 'limit',
		},
		'custom_models': custom_models
	}

	return json.dumps(base_info), json.dumps(postage_info), json.dumps(models_info), json.dumps(image_info)

def __format_resp_data(actual, corp_id):
	actual['remark'] = actual['detail']
	actual['postage_type'] = __postage_id2name(actual['postage_id'], corp_id)
	actual['price'] = actual['price_info']['display_price']
	actual['limit_zone_name'] = __limit_zone_id2name(actual['limit_zone'], corp_id)
	actual['limit_zone_type'] = __limit_type_number2name(actual['limit_zone_type'])
	actual['images'] = __format_resp_image_info(actual['images'])
	actual['stock'] = actual['stocks'][0] if isinstance(actual['stocks'], list) else actual['stocks']
	actual['has_product_model'] = bool(actual.get('models', False))
	actual['models'] = __format_resp_models_info(actual.get('models', []))

	return actual

@when(u"{user}创建商品分类为'{classification_name}'的待审核商品")
def step_impl(context, user, classification_name):
	datas = json.loads(context.text)
	corp_id = context.corp.id
	for data in datas:
		data['classification'] = classification_name
		base_info, postage_info, models_info, image_info = __format_post_data(context, data)
		response = context.client.put('/product/pre_product/', {
			'corp_id': corp_id,
			'base_info': base_info,
			'logistics_info': postage_info,
			'models_info': models_info,
			'image_info': image_info
		})
		bdd_util.assert_api_call_success(response)

@when(u"{user}编辑待审核商品信息")
def step_impl(context, user):
	datas = json.loads(context.text)
	corp_id = context.corp.id
	for data in datas:
		product_id = __product_names2ids_str([data['name']])[0]
		base_info, postage_info, models_info, image_info = __format_post_data(context, data)
		response = context.client.post('/product/pre_product/', {
			'corp_id': corp_id,
			'product_id': product_id,
			'base_info': base_info,
			'logistics_info': postage_info,
			'models_info': models_info,
			'image_info': image_info
		})
		bdd_util.assert_api_call_success(response)

@when(u"{user}编辑已审核商品信息")
def step_impl(context, user):
	datas = json.loads(context.text)
	corp_id = context.corp.id
	for data in datas:
		product_id = __product_names2ids_str([data['name']])[0]
		base_info, postage_info, models_info, image_info = __format_post_data(context, data)
		response = context.client.put('/product/product_unverified/', {
			'corp_id': corp_id,
			'product_id': product_id,
			'base_info': base_info,
			'logistics_info': postage_info,
			'models_info': models_info,
			'image_info': image_info
		})
		bdd_util.assert_api_call_success(response)

@Then(u"{user}查看已审核商品详情")
def step_impl(context, user):
	datas = json.loads(context.text)
	if context.corp.is_weizoom_corp:
		api = '/product/pre_product/'
	else:
		api = '/product/product_unverified/'

	for data in datas:
		product_id = __product_names2ids_str([data['name']])[0]
		corp_id = context.corp.id if not context.corp.is_weizoom_corp else __get_product_owner_id(product_id)
		response = context.client.get(api, {
			'corp_id': corp_id,
			'product_id': product_id
		})

		actual = response.data
		__format_resp_data(actual, corp_id)

		bdd_util.assert_dict(data, actual)

@when(u"{user}审核通过待审核商品")
def step_impl(context, user):
	datas = json.loads(context.text)
	response = context.client.put('/product/verified_product/', {
		'corp_id': context.corp.id,
		'product_ids': json.dumps(__product_names2ids_str(datas))
	})
	bdd_util.assert_api_call_success(response)

@when(u"{user}审核通过商品更新")
def step_impl(context, user):
	datas = json.loads(context.text)
	response = context.client.post('/product/verified_product/', {
		'corp_id': context.corp.id,
		'product_ids': json.dumps(__product_names2ids_str(datas))
	})
	bdd_util.assert_api_call_success(response)

@then(u"{user}查看待审核商品列表")
def step_impl(context, user):
	expected = bdd_util.table2list(context)
	response = context.client.get('/product/pre_products/', {
		'corp_id': context.corp.id
	})

	actual = response.data['rows']

	for row in actual:
		row['classification'] = row['classification_nav']
		row['created_time'] = u'创建时间'
		row['operation'] = __get_operations(context, row['status'], row['is_accepted'])
		row['status'] = __get_product_status_text(row['status'], row['is_accepted'])
		row['stock'] = __get_stocks_area(row['stocks'])
		row['price'] = __format_price_area(row['price_info'])
		row['owner_name'] = 'jobs'#TODO

	bdd_util.assert_list(expected, actual)

@then(u"{user}查看待审核商品更新列表")
def step_impl(context, user):
	expected = bdd_util.table2list(context)
	response = context.client.get('/product/pre_products/', {
		'corp_id': context.corp.id
	})
	actual = response.data['rows']
	new_rows = []
	for row in actual:
		if row['status'] == mall_models.PRODUCT_STATUS['SUBMIT'] and row['is_accepted']:
			new_rows.append({
				'id': row['id'],
				'owner_name': u'jobs',
				'operation': u'商品更新 驳回修改',
				'name': row['name'],
				'price': __format_price_area(row['price_info']),
				'stocks': __get_stocks_area(row['stocks']),
				'status': __get_product_status_text(row['status'], row['is_accepted']),
				'classification': row['classification_nav']
			})
	bdd_util.assert_list(expected, new_rows)

@when(u"{user}提交商品审核")
def step_impl(context, user):
	datas = json.loads(context.text)
	product_ids = __product_names2ids_str(datas)
	for product_id in product_ids:
		response = context.client.put('/product/pending_product/', {
			'corp_id': context.corp.id,
			'product_id': product_id
		})

		bdd_util.assert_api_call_success(response)

@when(u"{user}提交商品编辑审核")
def step_impl(context, user):
	datas = json.loads(context.text)
	product_ids = __product_names2ids_str(datas)
	for product_id in product_ids:
		response = context.client.put('/product/pending_product/', {
			'corp_id': context.corp.id,
			'product_id': product_id
		})

		bdd_util.assert_api_call_success(response)

@when(u"{user}删除待审核商品")
def step_impl(context, user):
	datas = json.loads(context.text)
	product_ids = __product_names2ids_str(datas)
	for product_id in product_ids:
		response = context.client.delete('/product/pre_product/', {
			'corp_id': context.corp.id,
			'product_id': product_id
		})

		bdd_util.assert_api_call_success(response)

@Then(u"{user}查看待更新商品'{product_name}'的对比详情")
def step_impl(context, user, product_name):
	data = json.loads(context.text)
	product_id = __product_names2ids_str([product_name])[0]
	expected_before_data = data['before']
	expected_after_data = data['after']

	corp_id = __get_product_owner_id(product_id)

	before_response = context.client.get('/product/pre_product/', {
		'corp_id': context.corp.id,
		'product_id': product_id
	})

	after_response = context.client.get('/product/product_unverified/', {
		'corp_id': context.corp.id,
		'product_id': product_id
	})

	__format_resp_data(before_response.data, corp_id)
	__format_resp_data(after_response.data, corp_id)

	bdd_util.assert_dict(expected_before_data, before_response.data)
	bdd_util.assert_dict(expected_after_data, after_response.data)



