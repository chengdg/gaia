# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

def __get_cps_promoted_products(context, user, cps_promoted_product):
    user = mall_models.User.select().dj_where(username=user).first()
    corp_id = user.id
    data = {
        'corp_id': corp_id,
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


@then(u"{user}可以看到商品池推广商品列表有'{cps_promoted_product}'")
def step_impl(context, user, cps_promoted_product):
    __get_cps_promoted_products(context, user, cps_promoted_product)

