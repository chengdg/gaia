# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models
from business.mall.logistics.shipper import Shipper

import logging


PROVINCE2ID = dict([(p.name,p.id) for p in mall_models.Province.select()])
CITY2ID = dict([(c.name,c.id) for c in mall_models.City.select()])
DISTRICT2ID = dict([(d.name,d.id) for d in mall_models.District.select()])

ID2PROVINCE = dict([(p.id, p.name) for p in mall_models.Province.select()])
ID2CITY = dict([(c.id, c.name) for c in mall_models.City.select()])
ID2DISTRICT = dict([(d.id, d.name) for d in mall_models.District.select()])

@when(u"{user}添加发货人")
def step_impl(context, user):

    datas = json.loads(context.text)
    url = '/mall/shipper/?_method=put'

    corp_id = context.corp.id
    for data in datas :
        province_id = PROVINCE2ID[data['province']]
        city_id = CITY2ID[data['city']]
        district_id = DISTRICT2ID[data['district']]
        arg = {
            "corp_id" : corp_id,
            "name" : data['shipper'],
            "tel_number" : data['mobile_num'],
            "province" : province_id,
            "city" : city_id,
            "district" : district_id,
            "address" : data['particular_address'],
            "postcode" : data['post_code'],
            "company_name" : data['business_name'],
            "remark" : data['remark'],
            "is_active" : "false"
        }

        response = context.client.post(url, arg)
        bdd_util.assert_api_call_success(response)

@then(u"{user}能获得发货人列表")
def step_impl(context, user):  

    url = '/mall/shippers/?_method=get'
    expected = json.loads(context.text)

    response = context.client.get(url, {"corp_id": context.corp.id})
    shippers = response.data['shippers']
    actuals = []
    for shipper in shippers:
        province = ID2PROVINCE[int(shipper['province'])]
        city = ID2CITY[int(shipper['city'])]
        district = ID2DISTRICT[int(shipper['district'])]
        actuals.append({
                'shipper' : shipper['name'],
                'province' : province,
                'city' : city,
                'district' : district,
                'particular_address' : shipper['address'],
                'post_code' : shipper['postcode'],
                'business_name' : shipper['company_name'],
                'mobile_num' : shipper['tel_number'],
                'remark' : shipper['remark'],
            })

    bdd_util.assert_list(expected, actuals)

def __get_shipper_id(corp_id, name):
    shipper = mall_models.ShipperMessages.select().dj_where(owner_id=corp_id, name=name).get()
    return shipper.id


@when(u"{user}删除名称为'{name}'的发货人")
def step_impl(context, user,name):

    url = '/mall/shipper/?_method=delete'

    corp_id = context.corp.id
    id = __get_shipper_id(context.corp.id, name)

    arg ={
        "corp_id" : corp_id,
        "id" : id,
    }
    response = context.client.post(url, arg)
    bdd_util.assert_api_call_success(response)


@when(u"{user}编辑发货人'{name}'的信息")
def step_impl(context, user,name):
    data = json.loads(context.text)
    url = '/mall/shipper/?_method=post'

    corp_id = context.corp.id
    id = __get_shipper_id(context.corp.id, name)

    province_id = PROVINCE2ID[data['province']]
    city_id = CITY2ID[data['city']]
    district_id = DISTRICT2ID[data['district']]
    arg = {
        "corp_id" : corp_id,
        "id" : id,
        "name" : data['shipper'],
        "tel_number" : data['mobile_num'],
        "province" : province_id,
        "city" : city_id,
        "district" : district_id,
        "address" : data['particular_address'],
        "postcode" : data['post_code'],
        "company_name" : data['business_name'],
        "remark" : data['remark'],
        "is_active" : "false"
    }

    response = context.client.post(url, arg)
    bdd_util.assert_api_call_success(response)


@when(u"{user}启用名称为'{name}'的发货人")
def step_impl(context, user,name):

    url = '/mall/active_shipper/?_method=put'

    corp_id = context.corp.id
    id = __get_shipper_id(context.corp.id, name)

    arg = {
        "corp_id" : corp_id,
        "id" : id
    }

    response = context.client.post(url, arg)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得发货人是否启用列表")
def step_impl(context, user):  

    url = '/mall/shippers/?_method=get'
    expected = json.loads(context.text)

    response = context.client.get(url, {"corp_id": context.corp.id})
    shippers = response.data['shippers']
    actuals = []
    for shipper in shippers:
        is_use = shipper['is_active']
        actuals.append({
                'shipper' : shipper['name'],
                'is_use' : is_use,
            })

    bdd_util.assert_list(expected, actuals)


@then(u"{user}能获得指定发货人'{name}'的列表")
def step_impl(context, user,name):
    expected = json.loads(context.text)
    url = '/mall/shipper/?_method=get'

    corp_id = context.corp.id
    id = __get_shipper_id(context.corp.id, name)
    arg = {
        "corp_id" : corp_id,
        "id" : id
    }
    response = context.client.post(url, arg)
    shipper = response.data['shipper']
    actuals = []

    province = ID2PROVINCE[int(shipper['province'])]
    city = ID2CITY[int(shipper['city'])]
    district = ID2DISTRICT[int(shipper['district'])]
    actuals.append({
            'shipper' : shipper['name'],
            'province' : province,
            'city' : city,
            'district' : district,
            'particular_address' : shipper['address'],
            'post_code' : shipper['postcode'],
            'business_name' : shipper['company_name'],
            'mobile_num' : shipper['tel_number'],
            'remark' : shipper['remark'],
        })

    bdd_util.assert_list(expected, actuals)