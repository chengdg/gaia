# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@when(u"{user}添加商品分类")
def step_impl(context, user):
    classification_lists = json.loads(context.text)
    for classification_list in classification_lists:
        level = 1
        father_id = 0
        for classification in classification_list:
            data = {
                "name": classification,
                "level": level,
                "father_id": father_id
            }
            response = context.client.put('/mall/product_classification/', data)
            bdd_util.assert_api_call_success(response)
            father_id = response.data['id']
            level += 1


@then(u"{user}能获取商品分类列表")
def step_get_category(context, user):
    response = context.client.get('/mall/product_classifications/')

    product_classifications = response.data['product_classifications']
    father2child = dict([(classification['father_id'], classification) for classification in product_classifications])

    classification_name_lists = []
    for classification in product_classifications:
        if classification['father_id'] != 0:
            continue

        classification_name_list = []
        classification_name_list.append(classification['name'])

        while True:
            child_classification = father2child.get(classification['id'], None)
            if not child_classification:
                break

            classification_name_list.append(child_classification['name'])
            classification = child_classification
        classification_name_lists.append(classification_name_list)
    actual = classification_name_lists

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}删除商品分类'{classification_name}'")
def step_delete_category(context, user, classification_name):
    supplier = mall_models.Supplier.select().dj_where(owner_id=context.corp.id, name=supplier_name).get()

    data = {
        'corp_id': context.corp.id,
        'id': supplier.id
    }
    response = context.client.delete('/mall/supplier/', data)
    bdd_util.assert_api_call_success(response)