# -*- coding: utf-8 -*-
import json

from features.util import bdd_util
from behave import *
from db.mall import models as mall_models
from db.mall import promotion_models


def __add_premium_sale_promotion(context, user):
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
    promotions = promotion_models.Promotion.select().dj_where(name=promotion_name)
    data = {
        "corp_id": user.id,
        'ids': json.dumps([promotion.id for promotion in promotions])
    }
    response = context.client.delete('/promotion/active_premium_sale_promotion/', data)
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
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    print response
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    if assert_status == u'已结束':
        print 'fffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        assert_status = 2
    assert int(response.data.get('status')) == assert_status


@when(u"{user}创建一个买赠活动")
def step_impl(context, user):
    __add_premium_sale_promotion(context, user)


@then(u"{user}根据商品名搜索到新创建的买赠活动")
def step_impl(context, user):
    __search_premium_sale_promotion(context, user)


@when(u"{user}结束买赠活动")
def step_impl(context, user):
    __off_premium_sale_promotion(context, user)


@then(u"{user}查看买赠活动'{promotion_name}'状态是'{promotion_status}'")
def step_impl(context, user, promotion_name, promotion_status):
    __get_promotion_info(context, user, promotion_name, promotion_status)
