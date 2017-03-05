# -*- coding: utf-8 -*-
import json

from features.util import bdd_util
from behave import *
from db.mall import models as mall_models
from db.mall import promotion_models
from db.member import models as member_models


def __add_integral_sale_promotion(context, user):
    user = mall_models.User.select().dj_where(username=user).first()
    promotion_data = json.loads(context.text)
    promotion_data['corp_id'] = user.id

    product_name = promotion_data['product']
    premium_product_name = promotion_data['premium_product']

    product_id = mall_models.Product.select().dj_where(name=product_name).first().id
    premium_product_id = mall_models.Product.select().dj_where(name=premium_product_name).first().id

    promotion_info = {
        "name": promotion_data['name'],
        "promotion_title": promotion_data['promotion_title'],
        "type": "premium_sale",
        "member_grade": "",
        "start_date": promotion_data['start_date'],
        "end_date": promotion_data['end_date']
    }

    detail_info = {
        "premium_product_id": premium_product_id,
        "premium_count": promotion_data['premium_count'],
        "is_enable_cycle": promotion_data['is_enable_cycle'],
        "unit": promotion_data['unit'],
        "count": promotion_data['count']
    }

    product_info = {
        "product_ids": [product_id]
    }
    promotion_data = {
        "corp_id": user.id,
        "detail_info": json.dumps(detail_info),
        "product_info": json.dumps(product_info),
        "promotion_info": json.dumps(promotion_info)
    }
    response = context.client.put('/promotion/premium_sale_promotion/', promotion_data)

    bdd_util.assert_api_call_success(response)


def __search_premium_sale_promotion(context, user):
    user = mall_models.User.select().dj_where(username=user).first()
    product_name = json.loads(context.text).get('product')
    filters = {
        '__f-product_name-contains': product_name
    }
    data = {
        "corp_id": user.id,
        "filters": json.dumps(filters)
    }
    response = context.client.get('/promotion/premium_sale_promotions/', data)

    premium_sale_promotions = response.data.get('premium_sale_promotions')
    assert_success = False
    for promotion in premium_sale_promotions:

        if promotion.get('products_info')[0].get('name') == product_name:
            assert_success = True
            break
    assert assert_success


def __off_premium_sale_promotion(context, user):
    user = mall_models.User.select().dj_where(username=user).first()
    promotion_name = json.loads(context.text).get('name')
    promotion = promotion_models.Promotion.select().dj_where(name=promotion_name).first()
    data = {
        "corp_id": user.id,
        'id': promotion.id
    }
    response = context.client.delete('/promotion/active_promotion/', data)
    bdd_util.assert_api_call_success(response)


def __get_promotion_info(context, user, promotion_name, assert_status):
    user = mall_models.User.select().dj_where(username=user).first()
    promotions = promotion_models.Promotion.select().dj_where(name=promotion_name)
    promotion_ids = [promotion.id for promotion in promotions]
    data = {
        "corp_id": user.id,
        'id': max(promotion_ids)
    }
    response = context.client.get('/promotion/premium_sale_promotion/', data)
    if assert_status == u'已结束':
        assert_status = 2
    assert int(response.data.get('status')) == assert_status


@when(u"{user}创建积分应用活动")
def step_impl(context, user):
    user = bdd_util.get_user_for(user)
    promotion_data = json.loads(context.text)

    promotion_info = {
        "name": promotion_data['name'],
        "promotion_title": promotion_data.get('promotion_title', u'默认的促销标题'),
        "type": "integral_sale",
        "start_date": promotion_data.get('start_date', '2017-01-01 00:00'),
        "end_date": promotion_data.get('end_date', '2017-01-02 00:00')
    }

    #确定积分应用的详情信息
    detail_info = {
        "is_permanant_active": promotion_data.get("is_permanant_active", False),
    }
    rule_info = promotion_data.get("rule_info")
    if rule_info['type'] == 'fixed':
        #固定的统一折扣
        pass
    else:
        for rule in rule_info['rules']:
            member_grade = member_models.MemberGrade.select().dj_where(webapp_id=context.corp.webapp_id, name=rule['member_grade']).get()
            rule['member_grade_id'] = member_grade.id
    detail_info['rule_info'] = rule_info

    #确定商品信息
    product_ids = []
    for product_name in promotion_data['products']:
        product = mall_models.Product.select().dj_where(name=product_name).get()
        product_ids.append(product.id)
    product_info = {
        'product_ids': product_ids
    }

    data = {
        "corp_id": user.id,
        "detail_info": json.dumps(detail_info),
        "product_info": json.dumps(product_info),
        "promotion_info": json.dumps(promotion_info)
    }

    response = context.client.put('/promotion/integral_sale_promotion/', data)

    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得积分应用活动'{promotion_name}'的详情")
def step_impl(context, user, promotion_name):
    promotion_model = promotion_models.Promotion.select().dj_where(name=promotion_name).get()

    url = '/promotion/integral_sale_promotion/?corp_id=%s&id=%s' % (context.corp.id, promotion_model.id)
    response = context.client.get(url)

    #通用promotion信息
    promotion_info = response.data['promotion_info']
    actual = {
        "name": promotion_info['name'],
        "promotion_title": promotion_info['promotion_title'],
        "start_date": promotion_info["start_date"],
        "end_date": promotion_info["end_date"]
    }

    #integral sale的detail信息
    detail = response.data['detail']
    actual["is_permanant_active"] = detail['is_permanant_active']

    rule_info = {"type": detail["rule_type"]}
    actual["rule_info"] = rule_info
    if rule_info['type'] == 'fixed':
        rule = detail['rules'][0]
        rule_info['discount'] = rule['discount']
        rule_info['discount_money'] = rule['discount_money']
    else:
        for rule in detail['rules']:
            member_grade = member_models.MemberGrade.select().dj_where(webapp_id=context.corp.webapp_id, id=rule['member_grade_id']).get()
            rule['member_grade'] = member_grade.name
        rule_info['rules'] = detail['rules']

    #商品信息
    products_info = response.data['products_info']
    products = [product_info['name'] for product_info in products_info]
    actual['products'] = products

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual)

@then(u"{user}能获得积分应用活动列表")
def step_impl(context, user):
    url = '/promotion/integral_sale_promotions/?corp_id=%s' % context.corp.id
    response = context.client.get(url)

    integral_sales = response.data['integral_sale_promotions']

    actual = []
    for integral_sale in integral_sales:
        #通用promotion信息
        promotion_info = integral_sale['promotion_info']
        one_actual_data = {
            "name": promotion_info['name'],
            "promotion_title": promotion_info['promotion_title'],
            "start_date": promotion_info["start_date"],
            "end_date": promotion_info["end_date"]
        }

        #integral sale的detail信息
        detail = integral_sale['detail']
        one_actual_data["is_permanant_active"] = detail['is_permanant_active']

        rule_info = {"type": detail["rule_type"]}
        one_actual_data["rule_info"] = rule_info
        if rule_info['type'] == 'fixed':
            rule = detail['rules'][0]
            rule_info['discount'] = rule['discount']
            rule_info['discount_money'] = rule['discount_money']
        else:
            for rule in detail['rules']:
                member_grade = member_models.MemberGrade.select().dj_where(webapp_id=context.corp.webapp_id, id=rule['member_grade_id']).get()
                rule['member_grade'] = member_grade.name
            rule_info['rules'] = detail['rules']

        #商品信息
        products_info = integral_sale['products_info']
        products = [product_info['name'] for product_info in products_info]
        one_actual_data['products'] = products

        actual.append(one_actual_data)

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual)
