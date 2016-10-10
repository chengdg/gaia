# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

import logging

def __get_post_data_postage(postage):
    data = {
        'name': postage['name']
    }

    default_config = {
        'first_weight': postage['first_weight'],
        'first_weight_price': postage['first_weight_price'],
        'added_weight': postage.get('added_weight', '0'),
        'added_weight_price': postage.get('added_weight_price', '0')
    }
    data['default_config'] = json.dumps(default_config)

    #处理特殊地区运费
    if 'special_area' in postage:
        data['is_enable_special_config'] = 'true'
        special_configs = []
        for special_config_data in postage.get('special_area'):
            special_config = {
                "first_weight": special_config_data.get('first_weight', "1.0"),
                "first_weight_price": special_config_data.get('first_weight_price', "1.0"),
                "added_weight": special_config_data.get('added_weight', "1.0"),
                "added_weight_price": special_config_data.get('added_weight_price', "1.0")
            }
            special_config['destinations'] = special_config_data.get('to_the', '')
            special_configs.append(special_config)
        data['special_configs'] = json.dumps(special_configs)
    else:
        data['is_enable_special_config'] = 'false'
        data['special_configs'] = "[]"

    #处理包邮运费
    if 'free_postages' in postage:
        data['is_enable_free_config'] = 'true'
        free_postages = []
        for free_postage_data in postage.get('free_postages'):
            free_postage = {
                "condition": free_postage_data['condition'],
                "value": free_postage_data['value']
            }
            free_postage['destinations'] = free_postage_data.get('to_the', '')
            free_postages.append(free_postage)
        data['free_configs'] = json.dumps(free_postages)
    else:
        data['is_enable_free_config'] = 'false'
        data['free_configs'] = "[]"

    return data


def __create_postage(context, user):
    client = context.client
    postages = json.loads(context.text)
    for postage in postages:
        data = __get_post_data_postage(postage)
        data['corp_id'] = context.corp.id
        response = client.put('/mall/postage_config/', data)
        bdd_util.assert_api_call_success(response)

def __get_postage_config_id_for(corp_id, name):
    model = mall_models.PostageConfig.select().dj_where(owner_id=corp_id, name=name).get()
    return model.id

@when(u"{user}添加邮费配置")
def create_postage(context, user):
    __create_postage(context, user)


@given(u"{user}已添加运费配置")
def step_impl(context, user):
    __create_postage(context, user)


@then(u"{user}能获取邮费配置列表")
def step_impl(context, user):
    client = context.client
    response = context.client.get('/mall/postage_configs/?corp_id=%d' % context.corp.id)
    actual = response.data['postage_configs']
    for item in actual:
        item['postage_items'] = []
        default_config = item['default_config']

        if 'special_configs' in item:
            item['special_area'] = item['special_configs']
            for special_config in item['special_area']:
                special_config['to_the'] = special_config['destinations']
                item['postage_items'].append(special_config)

        if len(item['postage_items']) > 0:
            default_config['to_the'] = u'其他地区'
        else:
            default_config['to_the'] = u'全国'
        item['postage_items'].append(default_config)
                
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}修改'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    postage = json.loads(context.text)
    data = __get_post_data_postage(postage)
    config_id = __get_postage_config_id_for(context.corp.id, postage_name)
    data['corp_id'] = context.corp.id
    data['id'] = config_id

    response = context.client.post('/mall/postage_config/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获取'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    config_id = __get_postage_config_id_for(context.corp.id, postage_name)
    response = context.client.get('/mall/postage_config/?corp_id=%d&id=%d' % (context.corp.id, config_id))

    actual = response.data
    default_config = actual['default_config']
    actual['first_weight'] = default_config['first_weight']
    actual['first_weight_price'] = default_config['first_weight_price']
    actual['added_weight'] = default_config['added_weight']
    actual['added_weight_price'] = default_config['added_weight_price']

    if 'special_configs' in actual:
        actual['special_area'] = actual['special_configs']
        for special_config in actual['special_area']:
            special_config['to_the'] = special_config['destinations']

    if 'free_configs' in actual:
        actual['free_postages'] = actual['free_configs']
        for free_config in actual['free_postages']:
            free_config['to_the'] = free_config['destinations']

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}选择'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    config_id = __get_postage_config_id_for(context.corp.id, postage_name)
    data = {'corp_id': context.corp.id, 'postage_config_id': config_id }
    response = context.client.put('/mall/active_postage_config/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除'{postage_name}'运费配置")
def step_impl(context, user, postage_name):
    config_id = __get_postage_config_id_for(context.corp.id, postage_name)
    data = {'corp_id': context.corp.id, 'id': config_id }
    response = context.client.delete('/mall/postage_config/', data)
    bdd_util.assert_api_call_success(response)

