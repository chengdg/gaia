# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

@given(u"{user}已添加商品规格")
def step_add_model_property(context, user):
    product_model_properties = json.loads(context.text)
    for property in product_model_properties:
        __add_product_model_property(context, property)


@when(u"{user}添加商品规格")
def step_w_add_model_property(context, user):
    product_model_properties = json.loads(context.text)
    for property in product_model_properties:
        __add_product_model_property(context, property)


@then(u"{user}能获取商品规格'{product_model_property_name}'")
def step_get_model_property(context, user, product_model_property_name):
    expected = json.loads(context.text)
    actual = get_model_property_from_web_page(
        context,
        product_model_property_name)

    bdd_util.assert_dict(expected, actual)


@then(u"{user}能获取商品规格列表")
def step_get_model_property_list(context, user):
    response = context.client.get('/product/model_properties/?corp_id=%d' % context.corp.id)

    expected = json.loads(context.text)

    actual = []
    model_properties = response.data['product_model_properties']
    for model_property in model_properties:
        data = {
            "name": model_property['name'],
            "type": u'图片' if model_property['type'] == 'image' else u'文字'
        }
        data['values'] = model_property['values']
        for value in data['values']:
            value['image'] = value['pic_url']
        actual.append(data)

    bdd_util.assert_list(expected, actual)


@when(u"{user}更新商品规格'{product_model_property_name}'为")
def step_update_model_property(context, user, product_model_property_name):
    db_model_property = mall_models.ProductModelProperty.select().dj_where(
        owner_id=context.corp.id,
        name=product_model_property_name,
        is_deleted=False
    ).get()
    property_id = db_model_property.id

    model_property = json.loads(context.text)

    # 更新name
    data = {
        "corp_id": context.corp.id,
        "id": property_id,
        "field": 'name',
        "value": model_property['name']
    }
    response = context.client.post('/product/model_property/', data)
    bdd_util.assert_api_call_success(response)

    #更新type
    data = {
        "corp_id": context.corp.id,
        "id": property_id,
        "field": 'type',
        "value": 'text'
    }
    type = model_property.get('type', None)
    if type == u'图片':
        data['value'] = 'image'
    response = context.client.post('/product/model_property/', data)
    bdd_util.assert_api_call_success(response)

    #处理add_values
    for value in model_property.get('add_values', []):
        if 'image' in value:
            value['pic_url'] = value['image']
        else:
            value['pic_url'] = ''
        value['model_property_id'] = property_id
        value['corp_id'] = context.corp.id
        response = context.client.put('/product/model_property_value/', value)
        bdd_util.assert_api_call_success(response)

    #处理delete_values
    for value in model_property.get('delete_values', []):
        db_model_prop_val = mall_models.ProductModelPropertyValue.select().dj_where(
            property=db_model_property,
            name=value['name'],
            is_deleted=False
        ).get()
        data = {
            'corp_id': context.corp.id,
            'id': db_model_prop_val.id
        }
        response = context.client.delete('/product/model_property_value/', data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品规格'{product_model_property_name}'")
def step_delete_model_property(context, user, product_model_property_name):
    db_model_property = mall_models.ProductModelProperty.select().dj_where(
        owner_id=context.corp.id,
        name=product_model_property_name,
        is_deleted=False
    ).get()

    data = {
        'corp_id': context.corp.id,
        'id': db_model_property.id
    }
    response = context.client.delete('/product/model_property/', data)
    bdd_util.assert_api_call_success(response)


def __add_product_model_property(context, model_property):
    # 创建product model property
    data = {
        "corp_id": context.corp.id,
        "name": model_property['name'],
        "type": "image" if model_property.get('type', u'文字') == u'图片' else 'text'
    }
    response = context.client.put('/product/model_property/', data)
    bdd_util.assert_api_call_success(response)

    model_property_id = response.data['product_model_property']['id']

    # 处理value
    for value in model_property['values']:
        if 'image' in value:
            value['pic_url'] = value['image']
        else:
            value['pic_url'] = ''
        value['corp_id'] = context.corp.id
        value['model_property_id'] = model_property_id
        response = context.client.put('/product/model_property_value/', value)
        bdd_util.assert_api_call_success(response)

