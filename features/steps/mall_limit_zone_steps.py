#-*- coding:utf-8 -*-

import types
import json

from behave import *
from features.util import bdd_util

from db.mall.models import ProductLimitZoneTemplate, City, Province

@then(u"{user}能获得限定区域列表")
def step_impl(context, user):
    url = '/mall/limit_zones/'

    response = context.client.get(url, {"corp_id": context.corp.id})

    limit_zones = response.data['limit_zones']
    expected = json.loads(context.text)
    actual = []
    for limit_zone in limit_zones:
        template_data = {}
        template_data['name'] = limit_zone['name']
        limit_area = []
        for zone in limit_zone['zones']:
            zone_data = {}
            if zone['zone_name'] in [u'直辖市', u'其它']:
                zone_data['area'] = zone['zone_name']
                province_list = []
                for province in zone['provinces']:
                    province_list.append(province['province_name'])
                zone_data['province'] = province_list
                limit_area.append(zone_data)
            else:
                for province in zone['provinces']:
                    zone_data = {}
                    zone_data['area'] = province['zone_name']
                    zone_data['province'] = province['province_name']
                    zone_data['city'] = []
                    for city in province['cities']:
                        zone_data['city'].append(city['city_name'])
                    limit_area.append(zone_data)
        template_data['limit_area'] = limit_area
        actual.append(template_data)

    bdd_util.assert_list(expected, actual)

@when(u"{user}添加限定区域配置")
def step_impl(context, user):
    data = json.loads(context.text)
    url = '/mall/limit_zone/?_method=put'

    template_name = data['name']
    provinces = []
    cities = []
    for limit_area in data['limit_area']:
        if type(limit_area['province']) is types.UnicodeType:
            provinces.append(limit_area['province'])
        if type(limit_area['province']) is types.ListType:
            provinces += limit_area['province']
        if limit_area.has_key('city'):
            cities += limit_area['city']
    province_ids = []

    for province in provinces:
        province_ids.append(filter(lambda p: province in p.name, Province.select())[0].id)
    city_ids = [c.id for c in City.select().dj_where(name__in=cities)]
    args = {
        'corp_id': context.corp.id,
        'name': template_name,
        'limit_provinces': json.dumps([str(id) for id in province_ids]),
        'limit_cities': json.dumps([str(id) for id in city_ids])
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

@when(u"{user}修改'{template_name}'限定区域配置")
def step_impl(context, user, template_name):
    template_id = ProductLimitZoneTemplate.select().dj_where(owner=context.corp.id, name=template_name).first().id

    data = json.loads(context.text)
    url = '/mall/limit_zone/'

    template_name = data['name']
    provinces = []
    cities = []
    for limit_area in data['limit_area']:
        if type(limit_area['province']) is types.UnicodeType:
            provinces.append(limit_area['province'])
        if type(limit_area['province']) is types.ListType:
            provinces += limit_area['province']
        if limit_area.has_key('city'):
            cities += limit_area['city']
    province_ids = []

    for province in provinces:
        province_ids.append(filter(lambda p: province in p.name, Province.select())[0].id)
    city_ids = [c.id for c in City.select().dj_where(name__in=cities)]
    args = {
        'corp_id': context.corp.id,
        'id': template_id,
        'name': template_name,
        'limit_provinces': json.dumps([str(id) for id in province_ids]),
        'limit_cities': json.dumps([str(id) for id in city_ids])
    }
    response = context.client.post(url, args)
    bdd_util.assert_api_call_success(response)

@when(u"{user}删除'{name}'限定区域配置")
def step_impl(context, user, name):
    template_id = ProductLimitZoneTemplate.select().dj_where(owner=context.corp.id, name=name).first().id
    url = "/mall/limit_zone/?_method=delete"

    response = context.client.post(url, {'id': template_id, 'corp_id': context.corp.id})
    bdd_util.assert_api_call_success(response)