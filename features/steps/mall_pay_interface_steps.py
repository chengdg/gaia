# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

import logging

from features.util import http

def __fill_post_data(pay_interface):
    data = {}
    data['is_active'] = "false" if pay_interface.get('is_active', '') == u'停用' else "true"

    type = pay_interface['type']
    if type == u'微信支付':
        data['type'] = mall_models.PAY_INTERFACE_WEIXIN_PAY
        version = pay_interface.get('version', 2)
        if version == 2 or version == 'V2' or version == 'v2':  # v2
            data['pay_version'] = 'v2'
            data['app_id'] = pay_interface.get('weixin_appid', '1')
            data['partner_id'] = pay_interface.get('weixin_partner_id', '2')
            data['partner_key'] = pay_interface.get('weixin_partner_key', '3')
            data['paysign_key'] = pay_interface.get('weixin_sign', '4')
        else:  # v3
            data['pay_version'] = 'v3'
            data['app_id'] = pay_interface.get('weixin_appid', '11')
            data['app_secret'] = pay_interface.get('app_srcret', '22')
            data['mch_id'] = pay_interface.get('mch_id', '33')  # mch_id
            data['api_key'] = pay_interface.get('api_key', '44')  # api_key
            data['paysign_key'] = pay_interface.get('paysign_key', '55')
    elif type == u'支付宝':
        data['type'] = mall_models.PAY_INTERFACE_ALIPAY
        data['partner'] = pay_interface.get('partner', '1')
        data['key'] = pay_interface.get('key', '2')
        data['ali_public_key'] = pay_interface.get('ali_public_key', '3')
        data['private_key'] = pay_interface.get('private_key', '4')
        data['seller_email'] = pay_interface.get('seller_email', '5@a.com')
    elif type == u'货到付款':
        data['type'] = mall_models.PAY_INTERFACE_COD
    elif type == u'微众卡支付':
        data['type'] = mall_models.PAY_INTERFACE_WEIZOOM_COIN
    else:
        pass
    return data


def __add_pay_interface(context, pay_interface):
    data = __fill_post_data(pay_interface)

    db_pay_interface = mall_models.PayInterface.select().dj_where(owner_id=context.corp.id, type=data['type']).get()
    data['corp_id'] = context.corp.id
    data['id'] = db_pay_interface.id
    data['is_active'] = "true"

    type = pay_interface['type']
    if type == u'微信支付':
        response = context.client.post('/mall/weixin_pay_interface/', data)
    elif type == u'支付宝':
        response = context.client.post('/mall/ali_pay_interface', data)
    else:
        response = context.client.post('/mall/pay_interface_activity/', data)

    return response

@when(u"{user}添加支付方式")
def step_impl(context, user):
    client = context.client
    pay_interfaces = json.loads(context.text)
    response = context.client.get('/mall/pay_interfaces/?corp_id=%d' % context.corp.id)
    for pay_interface in pay_interfaces:
         __add_pay_interface(context, pay_interface)


@then(u"{user}能获得支付方式")
def step_impl(context, user):
    """
    列出支付方式的详细信息
    """
    url = '/mall/pay_interfaces/?corp_id=%d' % context.corp.id
    response = context.client.get(url)

    expected = json.loads(context.text)
    if expected['type'] == u'微信支付':
        pay_interface_type = 'weixin_pay'
    elif expected['type'] == u'货到付款':
        pay_interface_type = 'cod'
    elif expected['type'] == u'微众卡支付':
        pay_interface_type = 'weizoom_coin'
    elif expected['type'] == u'支付宝':
        pay_interface_type = 'alipay'

    target_pay_interface = None
    for this_pay_interface in response.data['pay_interfaces']:
        if this_pay_interface['type'] == pay_interface_type:
            target_pay_interface = this_pay_interface
            break

    actual = target_pay_interface
    actual['is_active'] = u'启用' if actual['is_active'] else u'停用'

    actual_config = actual['config']
    actual_type = actual['type']
    if actual_type == 'weixin_pay':
        actual['type'] = u'微信支付'
        if actual['config']['version'] == 'v2':
            #v2
            actual['version'] = 2
            actual['weixin_appid'] = actual_config['app_id']
            actual['weixin_partner_id'] = actual_config['partner_id']
            actual['weixin_partner_key'] = actual_config['partner_key']
            actual['weixin_sign'] = actual_config['paysign_key']
        else:
            #v3
            actual['version'] = 3
            actual['weixin_appid'] = actual_config['app_id']
            actual['mch_id'] = actual_config['mch_id']
            actual['api_key'] = actual_config['api_key']
            actual['paysign_key'] = actual_config['paysign_key']
    elif actual_type == 'alipay':
        actual['type'] = u'支付宝'
        actual['partner'] = actual_config['partner']
        actual['key'] = actual_config['key']
        actual['ali_public_key'] = actual_config['ali_public_key']
        actual['private_key'] = actual_config['private_key']
        actual['seller_email'] = actual_config['seller_email']
    elif actual_type == 'cod':
        actual['type'] = u'货到付款'
    elif actual_type == 'weizoom_coin':
        actual['type'] = u'微众卡支付'
    else:
        pass

    print("expected: {}".format(expected))
    print("actual: {}".format(actual))

    bdd_util.assert_dict(expected, actual)


def __type_to_name(type):
    """
    将type转成名字
    """
    name = None
    if type == 'weixin_pay':
        name = u'微信支付'
    elif type == 'cod':
        name = u'货到付款'
    elif type == 'alipay':
        name = u'支付宝'
    elif type == 'weizoom_coin':
        name = u'微众卡支付'
    return name


def __name_to_dbtype(name):
    """
    将支付方式的名字转成ID
    """
    pay_interface_type = None
    if name == u'微信支付':
        pay_interface_type = mall_models.PAY_INTERFACE_WEIXIN_PAY
    elif name == u'货到付款':
        pay_interface_type = mall_models.PAY_INTERFACE_COD
    elif name == u'微众卡支付':
        pay_interface_type = mall_models.PAY_INTERFACE_WEIZOOM_COIN
    elif name == u'支付宝':
        pay_interface_type = mall_models.PAY_INTERFACE_ALIPAY
    return pay_interface_type


@then(u"{user}能获得支付方式列表")
def step_impl(context, user):
    """
    只列出支付方式列表
    """
    expected = json.loads(context.text)

    response = context.client.get('/mall/pay_interfaces/?corp_id=%d' % context.corp.id)
    interfaces = list(response.data['pay_interfaces'])
    actual = []
    for pay_interface in interfaces:

        _actual = {
            'type': __type_to_name(pay_interface['type']),
            'is_active': u'启用' if pay_interface['is_active'] else u'停用'
        }
        actual.append(_actual)

    bdd_util.assert_list(expected, actual)


@when(u"{user}'{action}'支付方式'{pay_interface_name}'")
def impl_step(context, user, action, pay_interface_name):
    """
    启用、停用支付方式
    """
    db_type = __name_to_dbtype(pay_interface_name)
    db_pay_interface = mall_models.PayInterface.select().dj_where(owner_id=context.corp.id, type=db_type).get()

    data = {
        'corp_id': context.corp.id,
        'id': db_pay_interface.id,
        'is_active': 'true' if action == u'启用' else 'false'
    }

    response = context.client.post('/mall/pay_interface_activity/', data)
    bdd_util.assert_api_call_success(response)
