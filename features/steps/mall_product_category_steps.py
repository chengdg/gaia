# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@given(u"{user}已添加商品分组")
def step_add_category(context, user):
    product_categories = json.loads(context.text)
    for product_category in product_categories:
        data = product_category
        data['corp_id'] = context.corp.id
        response = context.client.put('/mall/category/', data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}添加商品分组")
def step_impl(context, user):
    product_categories = json.loads(context.text)
    for product_category in product_categories:
        data = product_category
        data['corp_id'] = context.corp.id
        if 'products' in product_category:
            product_ids = []
            for product_name in product_category['products']:
                product_model = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()
                product_ids.append(product_model.id)
            data['product_ids'] = product_ids

        response = context.client.put('/mall/category/', data)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取商品分组列表")
def step_get_category(context, user):
    response = context.client.get('/mall/categories/?corp_id=%d&category_id=0&return_product=true' % context.corp.id)
    
    for category in response.data['categories']:
        for product in category['products']:
            if product['status'] == 'off_shelf':
                product['status'] = u'待售'
            elif product['status'] == 'on_shelf':
                product['status'] = u'在售'
            else:
                pass
    actual = response.data['categories']

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}更新商品分组'{category_name}'为")
def step_update_category(context, user, category_name):
    existed_product_category = mall_models.ProductCategory.select().dj_where(owner=context.corp.id, name=category_name).get()
    new_product_category = json.loads(context.text)
    data = {
        'corp_id': context.corp.id,
        'category_id': existed_product_category.id,
        'field': 'name',
        'value': new_product_category['name']
    }
    response = context.client.post('/mall/category/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品分组'{category_name}'")
def step_delete_category(context, user, category_name):
    product_category = mall_models.ProductCategory.select().dj_where(
        owner_id = context.corp.id,
        name = category_name
    ).get()

    data = {
        'corp_id': context.corp.id,
        'category_id': product_category.id
    }
    response = context.client.delete('/mall/category/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}从商品分组'{category_name}'中删除商品'{product_name}'")
def step_delete_p_in_categroy(context, user, category_name, product_name):
    existed_product_category = mall_models.ProductCategory.select().dj_where(owner=context.corp.id, name=category_name).get()
    existed_product = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()

    data = {
        'corp_id': context.corp.id,
        'category_id': existed_product_category.id,
        'product_id': existed_product.id
    }
    url = '/mall/category_product/'
    response = context.client.delete(url, data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得商品分组'{category_name}'的可选商品集合为")
def step_get_p_from_category(context, user, category_name):
    existed_product_category = ProductCategoryFactory(name=category_name)
    url = '/mall2/api/category_list/?id={}'.format(existed_product_category.id)
    response = context.client.get(url)

    actual = json.loads(response.content)['data']['items']
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}向商品分组'{category_name}'中添加商品")
def step_add_p_to_category(context, user, category_name):
    existed_product_category = mall_models.ProductCategory.select().dj_where(owner=context.corp.id, name=category_name).get()

    product_names = json.loads(context.text)
    product_ids = []
    for product_name in product_names:
        product_model = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()
        product_ids.append(product_model.id)

    data = {
        'corp_id': context.corp.id,
        'category_id': existed_product_category.id,
        'product_ids': json.dumps(product_ids)
    }
    response = context.client.post('/mall/category_products/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}更新商品分组'{category_name}'中商品'{product_name}'的排序为'{position}'")
def step_impl(context, user, category_name, product_name, position):
    existed_product_category = mall_models.ProductCategory.select().dj_where(owner=context.corp.id, name=category_name).get()
    existed_product = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()

    data = {
        'corp_id': context.corp.id,
        'category_id': existed_product_category.id,
        'product_id': existed_product.id,
        'field': 'position',
        'value': position
    }
    response = context.client.post('/mall/category_product/', data)
    bdd_util.assert_api_call_success(response)

