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

        if 'type' in data:
            if data['type'] == u'固定低价':
                data['type'] = 'fixed'
            elif data['type'] == u'首月55分成':
                data['type'] = 'divide'
                original_divide_info = data.get('divide_info', None)
                data['divide_info'] = json.dumps({
                    "divide_money": original_divide_info['divide_money'] if original_divide_info else 1,
                    "basic_rebate": original_divide_info['basic_rebate'] if original_divide_info else 2,
                    "rebate": original_divide_info['rebate'] if original_divide_info else 3
                })
            elif data['type'] == u'零售返点':
                data['type'] = 'retail'
                original_retail_info = data.get('retail_info', None)
                data['retail_info'] = json.dumps({
                    "rebate": original_retail_info['rebate'] if original_retail_info else 3
                })
        data['corp_id'] = context.corp.id
        response = context.client.put('/mall/supplier/', data)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取供应商列表")
def step_get_category(context, user):
    response = context.client.get('/mall/suppliers/?corp_id=%d' % context.corp.id)
    
    actual = response.data['suppliers']

    for supplier in actual:
        if supplier['type'] == 'fixed':
            supplier['type'] = u'固定低价'
        elif supplier['type'] == 'divide':
            supplier['type'] = u'首月55分成'
            supplier['divide_info'] = supplier['divide_type_info']
        elif supplier['type'] == 'retail':
            supplier['type'] = u'零售返点'
            supplier['retail_info'] = supplier['retail_type_info']
        else:
            pass

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