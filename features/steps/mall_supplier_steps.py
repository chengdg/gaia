# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@when(u"{user}添加供应商")
def step_impl(context, user):
    suppliers = json.loads(context.text)
    for supplier in suppliers:
        data = supplier
        if not 'responsible_person' in data:
            data['responsible_person'] = u'%s的负责人' % data['name']
        if not 'supplier_tel' in data:
            data['supplier_tel'] = '13811223344'
        if not 'supplier_address' in data:
            data['supplier_address'] = u'%s的公司地址' % data['name']
        data['corp_id'] = context.corp.id
        response = context.client.put('/mall/supplier/', data)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取供应商列表")
def step_get_category(context, user):
    response = context.client.get('/mall/suppliers/?corp_id=%d' % context.corp.id)
    
    # for category in response.data['suppliers']:
    #     for product in category['products']:
    #         if product['status'] == 'off_shelf':
    #             product['status'] = u'待售'
    #         elif product['status'] == 'on_shelf':
    #             product['status'] = u'在售'
    #         else:
    #             pass
    actual = response.data['suppliers']

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}更新供应商'{supplier_name}'为")
def step_update_category(context, user, supplier_name):
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


@when(u"{user}删除供应商'{supplier_name}'")
def step_delete_category(context, user, supplier_name):
    supplier = mall_models.Supplier.select().dj_where(owner_id=context.corp.id, name=supplier_name).get()

    data = {
        'corp_id': context.corp.id,
        'id': supplier.id
    }
    response = context.client.delete('/mall/supplier/', data)
    bdd_util.assert_api_call_success(response)