# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models
from business.mall.logistics.shipper import Shipper

import logging

@when(u"{user}添加电子面单账号配置")
def step_impl(context, user):

    datas = json.loads(context.text)
    url = '/mall/express_bill_account/?_method=put'

    corp_id = context.corp.id
    for data in datas :
        arg = {
            "corp_id" : corp_id,
            "express_name" : data['name'],
            "customer_name" : data['Customer_name'],
            "customer_pwd" : data['Custome_password'],
            "logistics_number" : data['monthcode'],
            "sendsite" : data['send_site'],
            "remark" : data['remark'],
        }

        response = context.client.post(url, arg)
        bdd_util.assert_api_call_success(response)

@then(u"{user}能获得电子面单账号列表")
def step_impl(context, user):  

    url = '/mall/express_bill_accounts/?_method=get'
    expected = json.loads(context.text)

    response = context.client.get(url, {"corp_id": context.corp.id})
    express_bill_accounts = response.data['express_bill_accounts']
    actuals = []
    for express_bill_account in express_bill_accounts:
        actuals.append({
            "name" : express_bill_account['express_name'],
            "Customer_name" : express_bill_account['customer_name'],
            "Custome_password" : express_bill_account['customer_pwd'],
            "monthcode" : express_bill_account['logistics_number'],
            "send_site" : express_bill_account['sendsite'],
            "remark" : express_bill_account['remark'],
        })

    bdd_util.assert_list(expected, actuals)

def __get_express_bill_account_id(corp_id, name):
    express_bill_account= mall_models.ExpressBillAccount.select().dj_where(owner_id=corp_id, express_name=name).get()
    return express_bill_account.id

@when(u"{user}删除物流公司为'{name}'的账号配置")
def step_impl(context, user,name):

    url = '/mall/express_bill_account/?_method=delete'

    corp_id = context.corp.id
    id = __get_express_bill_account_id(context.corp.id, name)

    arg ={
        "corp_id" : corp_id,
        "id" : id,
    }
    response = context.client.post(url, arg)
    bdd_util.assert_api_call_success(response)

@when(u"{user}编辑物流公司为'{name}'的账号配置")
def step_impl(context, user,name):
    data = json.loads(context.text)
    url = '/mall/express_bill_account/?_method=post'

    corp_id = context.corp.id
    id = __get_express_bill_account_id(context.corp.id, name)
    
    arg = {
        "corp_id" : corp_id,
        "id" : id,
        "express_name" : data['name'],
        "customer_name" : data['Customer_name'],
        "customer_pwd" : data['Custome_password'],
        "logistics_number" : data['monthcode'],
        "sendsite" : data['send_site'],
        "remark" : data['remark'],
        }

    response = context.client.post(url, arg)
    bdd_util.assert_api_call_success(response)