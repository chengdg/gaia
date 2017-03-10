# -*- coding: utf-8 -*-
import json

from features.util import bdd_util
from behave import *
from db.mall import models as mall_models
from db.mall import promotion_models
from db.member import models as member_models

def __add_coupon_rule(context, webapp_owner_name):
    coupon_rules = json.loads(context.text)
    if type(coupon_rules) == dict:
        coupon_rules = [coupon_rules]

    webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
    for coupon_rule in coupon_rules:
        name = coupon_rule['name']
        money = coupon_rule.get('money', 10.0)
        count = coupon_rule.get('count', 4)

        limit_counts = coupon_rule.get('limit_counts', -1)
        if limit_counts == u'无限':
            limit_counts = -1
        
        start_date = coupon_rule.get('start_date', u'今天')
        if u'天' in start_date:
            start_date = "{} 00:00".format(bdd_util.get_date_str(start_date))
        end_date = coupon_rule.get('end_date', u'1天后')
        if u'天' in end_date:
            end_date = "{} 00:00".format(bdd_util.get_date_str(end_date))
        
        remark = coupon_rule.get('description', '')  #使用说明
        note = coupon_rule.get('note', '')  #备注
        post_data = {
            'corp_id': context.corp.id,
            'name': name,
            'money': money,
            'coupon_count': count,
            'receive_limit_count': limit_counts,
            'start_date': start_date,
            'end_date': end_date,
            'remark': remark,
            'note': note
        }

        #处理"使用限制"
        using_limit_data = {
            "is_no_order_user_only": coupon_rule.get('is_no_order_user_only', False),
            "has_valid_restriction": False,
            "valid_restrictions": -1,
            "is_for_specific_products": False,
            "product_ids": []
        }
        if "using_limit" in coupon_rule:
            using_limit_data['type'] = True
            using_limit = coupon_rule['using_limit']
            end = using_limit.find(u"元")
            if end == -1:
                using_limit_data['valid_restrictions'] = -1
            else:
                using_limit_data['has_valid_restriction'] = True
                using_limit_data['valid_restrictions'] = int(using_limit[1:end])
        
        #处理商品信息
        if "coupon_product" in coupon_rule:
            using_limit_data['is_for_specific_products'] = True

            product_ids = []
            for product_name in coupon_rule['coupon_product'].split(','):
                product_ids.append(mall_models.Product.select().dj_where(name=product_name).get().id)

            using_limit_data['product_ids'] = product_ids

        post_data['using_limit'] = json.dumps(using_limit_data)

        response = context.client.put('/coupon/coupon_rule/', post_data)
        bdd_util.assert_api_call_success(response)

        if "coupon_id_prefix" in coupon_rule:
            latest_coupon_rule = promotion_models.CouponRule.select().order_by(-promotion_models.CouponRule.id)[0]
            index = 1
            coupon_id_prefix = coupon_rule['coupon_id_prefix']
            for coupon in promotion_models.Coupon.select().dj_where(coupon_rule_id=latest_coupon_rule.id):
                coupon_id = "%s%d" % (coupon_id_prefix, index)
                promotion_models.Coupon.update(coupon_id=coupon_id).dj_where(id=coupon.id).execute()
                index += 1

        # context.response = response

@when(u"{user}添加优惠券规则")
def step_impl(context, user):
    __add_coupon_rule(context, user)


@when(u"{user}更新优惠券规则'{coupon_rule_name}'为")
def step_impl(context, user, coupon_rule_name):
    model = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()

    update_data = json.loads(context.text)

    data = {
        'corp_id': context.corp.id,
        'id': model.id
    }

    field_map = {
        'name': 'name',
        'note': 'note',
        'description': 'remark'
    }
    for field in field_map:
        if field in update_data:
            data[field_map[field]] = update_data[field]

    response = context.client.post('/coupon/coupon_rule/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}使优惠券规则'{coupon_rule_name}'失效")
def step_impl(context, user, coupon_rule_name):
    model = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()

    data = {
        'corp_id': context.corp.id,
        'id': model.id
    }

    response = context.client.put('/coupon/disabled_coupon_rule/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除优惠券规则'{coupon_rule_name}'")
def step_impl(context, user, coupon_rule_name):
    model = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()

    data = {
        'corp_id': context.corp.id,
        'id': model.id
    }

    response = context.client.delete('/coupon/coupon_rule/', data)
    bdd_util.assert_api_call_success(response)

@when(u"{user}为优惠券'{coupon_rule_name}'增加'{count}'个库存")
def step_impl(context, user, coupon_rule_name, count):
    coupon_rule_model = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()
    current_coupons = list(promotion_models.Coupon.select().dj_where(coupon_rule_id=coupon_rule_model.id))

    #确认是否有prefix，如果coupon_id最后一个字符是整数，认为有prefix
    has_prefix = False
    last_coupon = current_coupons[-1]
    last_char = last_coupon.coupon_id[-1]
    try:
        from_index = int(last_char)
        coupon_id_prefix = last_coupon.coupon_id[:-1]
        has_prefix = True
    except:
        has_prefix = False

    data = {
        'corp_id': context.corp.id,
        'coupon_rule_id': coupon_rule_model.id,
        'count': count
    }

    response = context.client.put('/coupon/coupons/', data)
    bdd_util.assert_api_call_success(response)

    if has_prefix:
        index = from_index+1
        for i, coupon in enumerate(list(promotion_models.Coupon.select().dj_where(coupon_rule_id=coupon_rule_model.id))):
            if i + 1 <= from_index:
                continue

            coupon_id = "%s%d" % (coupon_id_prefix, index)
            promotion_models.Coupon.update(coupon_id=coupon_id).dj_where(id=coupon.id).execute()
            index += 1


@then(u"{user}获得优惠券规则'{coupon_rule_name}'")
def step_impl(context, user, coupon_rule_name):
    model = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()

    url = '/coupon/coupon_rule/?corp_id=%s&id=%s' % (context.corp.id, model.id)
    response = context.client.get(url)

    #通用promotion信息
    data = response.data
    using_limit = data['using_limit']
    valid_restrictions = ''
    if using_limit['has_valid_restriction']:
        valid_restrictions = u'满%s元可以使用' % using_limit['valid_restrictions']
    else:
        valid_restrictions = u'无限制'

    #处理商品
    coupon_product = ""
    if using_limit['is_for_specific_products']:
        products = mall_models.Product.select().dj_where(id__in=using_limit['product_ids'])
        coupon_product = ','.join([product.name for product in products])

    actual = {
        "name": data['name'],
        "status": data['status'],
        "money": data['money'],
        "limit_counts": data['receive_limit_count'],
        "using_limit": valid_restrictions,
        "count": data['coupon_count'],
        "start_date": data['start_date'],
        "end_date": data['end_date'],
        "description": data['remark'],
        "note": data['note'],
        "is_no_order_user_only": using_limit['is_no_order_user_only'],
        "is_for_specific_products": using_limit['is_for_specific_products'],
        "coupon_product": coupon_product,
        "remained_count": data['remained_count'],
        "use_count": data['use_count'],
        "receive_count": data['receive_count'],
        "receive_user_count": data['receive_user_count']
    }

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual)


@when(u"{user}批量删除优惠券")
def step_impl(context, user):
    coupon_bids = json.loads(context.text)
    coupon_ids = [coupon.id for coupon in promotion_models.Coupon.select().dj_where(coupon_id__in=coupon_bids)]
    
    data = {
        'corp_id': context.corp.id,
        'ids': json.dumps(coupon_ids)
    }

    response = context.client.delete('/coupon/coupons/', data)
    bdd_util.assert_api_call_success(response)


@then(u"{user}能获得优惠券规则列表")
def step_impl(context, user):
    url = '/coupon/coupon_rules/?corp_id=%s' % context.corp.id
    response = context.client.get(url)

    #通用promotion信息
    coupon_rules = response.data['coupon_rules']
    actual = []
    for data in coupon_rules:
        using_limit = data['using_limit']
        valid_restrictions = ''
        if using_limit['has_valid_restriction']:
            valid_restrictions = u'满%s元可以使用' % using_limit['valid_restrictions']
        else:
            valid_restrictions = u'无限制'

        #处理商品
        coupon_product = ""
        if using_limit['is_for_specific_products']:
            products = mall_models.Product.select().dj_where(id__in=using_limit['product_ids'])
            coupon_product = ','.join([product.name for product in products])

        one_actual = {
            "name": data['name'],
            "status": data['status'],
            "money": data['money'],
            "limit_counts": data['receive_limit_count'],
            "using_limit": valid_restrictions,
            "count": data['coupon_count'],
            "start_date": data['start_date'],
            "end_date": data['end_date'],
            "description": data['remark'],
            "note": data['note'],
            "is_no_order_user_only": using_limit['is_no_order_user_only'],
            "is_for_specific_products": using_limit['is_for_specific_products'],
            "coupon_product": coupon_product,
            "remained_count": data['remained_count'],
            "use_count": data['use_count'],
            "receive_count": data['receive_count'],
            "receive_user_count": data['receive_user_count']
        }
        actual.append(one_actual)

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual)


@then(u"{user}能获得优惠券'{coupon_rule_name}'的码库")
def step_impl(context, user, coupon_rule_name):
    model = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()

    url = '/coupon/coupons/?corp_id=%s&coupon_rule_id=%s' % (context.corp.id, model.id)
    response = context.client.get(url)

    #通用promotion信息
    coupons = response.data['coupons']
    actual = {}
    status2str = {
        'ungot': u'未领取',
        'unused': u'未使用',
        'used': u'已使用',
        'discard': u'作废',
        'expired': u'已过期',
        'disabled': u'已失效'
    }
    for coupon in coupons:
        data = {
            "money": coupon['money'],
            "status": status2str[coupon['status']],
            "consumer": ""
        }
        actual[coupon['bid']] = data

    expected = json.loads(context.text)

    bdd_util.assert_dict(expected, actual)
