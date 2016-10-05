# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@when(u"{user}添加属性模板")
def step_add_property(context, user):
    property_templates = json.loads(context.text)
    if not type(property_templates) == list:
        property_templates = [property_templates]

    for property_template in property_templates:
        property_template['title'] = property_template['name']
        for property in property_template['properties']:
            property['id'] = -1
            property['value'] = property['description']
        property_template['new_properties'] = json.dumps(property_template['properties'])
        property_template['corp_id'] = context.corp.id
        response = context.client.put('/product/property_template/', property_template)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取属性模板列表")
def step_get_property_list(context, user):
    response = context.client.get('/product/property_templates/?corp_id=%d' % context.corp.id)
    actual = response.data['templates']
    for template in actual:
        for template_property in template['properties']:
            template_property['description'] = template_property['value']

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@then(u"{user}能获取属性模板'{property_template_name}'")
def step_get_property(context, user, property_template_name):
    db_property_template = mall_models.ProductPropertyTemplate.select().dj_where(
        owner_id=context.corp.id,
        name=property_template_name
    ).get()

    url = '/product/property_template/?corp_id=%d&template_id=%d' % (context.corp.id, db_property_template.id)
    response = context.client.get(url)
    actual = response.data['template']
    for property in actual['properties']:
        property['description'] = property['value']

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}更新属性模板'{property_template_name}'")
def step_update_property(context, user, property_template_name):
    db_property_template = mall_models.ProductPropertyTemplate.select().dj_where(
        owner_id=context.corp.id,
        name=property_template_name
    ).get()

    property_template = json.loads(context.text)
    property_template['corp_id'] = context.corp.id
    property_template['id'] = db_property_template.id
    property_template['title'] = property_template['name']
    # 处理添加的property
    for property in property_template['add_properties']:
        property['id'] = -1
        property['value'] = property['description']
    property_template['new_properties'] = json.dumps(property_template['add_properties'])
    # 处理更新的property
    for property in property_template['update_properties']:
        db_property = mall_models.TemplateProperty.select().dj_where(
            owner_id=context.corp.id,
            name=property['original_name']
        ).get()
        property['id'] = db_property.id
        property['value'] = property['description']
        del property['original_name']
    property_template['update_properties'] = json.dumps(property_template['update_properties'])
    # 处理删除的property
    deleted_ids = []
    for property in property_template['delete_properties']:
        db_property = mall_models.TemplateProperty.select().dj_where(
            owner_id=context.corp.id,
            name=property['name']
        ).get()
        deleted_ids.append(db_property.id)
    property_template['deleted_ids'] = json.dumps(deleted_ids)

    response = context.client.post('/product/property_template/', property_template)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除属性模板'{property_template_name}'")
def step_delete_property(context, user, property_template_name):
    db_property_template = mall_models.ProductPropertyTemplate.select().dj_where(
        owner_id=context.corp.id,
        name=property_template_name
    ).get()

    data = {
        "corp_id": context.corp.id,
        "id": db_property_template.id
    }

    response = context.client.delete("/product/property_template/", data)
    bdd_util.assert_api_call_success(response)

