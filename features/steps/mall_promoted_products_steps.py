# -*- coding: utf-8 -*-
import json

from features.util import bdd_util
from behave import *
from db.mall import models as mall_models


def __get_cps_promoted_products(context, user, cps_promoted_product):
    user = mall_models.User.select().dj_where(username=user).first()
    data = {
        'corp_id': user.id,
        'product_status': 'pool'
    }
    response = context.client.get('/product/cps_promoted_products/', data)

    cps_promoted_products = response.data.get('products')
    assert_success = False
    for product in cps_promoted_products:

        if product.get('base_info').get('name') == cps_promoted_product:
            assert_success = True
            break
    assert assert_success


def __get_unprocessed_cps_promoted_products_count(context, user):
    user = mall_models.User.select().dj_where(username=user).first()
    data = {
        'corp_id': user.id,
    }
    response = context.client.get('/product/unprocessed_cps_promoted_products_count/', data)
    assert response.data.get('count') >= 3


def __processe_cps_promoted_products(context, user):
    user = mall_models.User.select().dj_where(username=user).first()
    product_names = json.loads(context.text)
    product_ids = [product.id for product in mall_models.Product.select().dj_where(name__in=product_names)]

    data = {
        'corp_id': user.id,
        'product_ids': json.dumps(product_ids)
    }
    response = context.client.put('/product/processed_cps_promoted_products/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}可以看到商品池推广商品列表有'{cps_promoted_product}'")
def step_impl(context, user, cps_promoted_product):
    __get_cps_promoted_products(context, user, cps_promoted_product)


@then(u"{user}可以查询到至少3个新增推广商品")
def step_impl(context, user):
    __get_unprocessed_cps_promoted_products_count(context, user)


@then(u"{user}处理推广商品")
def step_impl(context, user):
    __processe_cps_promoted_products(context, user)


