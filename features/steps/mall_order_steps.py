# -*- coding:utf-8 -*-

import types
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models



def get_order_id_by_bid(bid):

	return mall_models.Order.select().dj_where(order_id=bid).first().id

@then(u"{user}获得订单列表")
def step_impl(context, user):
	url = '/order/orders/?corp_id=%d' % context.corp.id
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	actual = response.data["orders"]




	# for o in actual:
	# 	o['order_no'] = o['bid']
	# 	o['methods_of_payment'] = mall_models.PAYTYPE2NAME[mall_models.PAYSTR2TYPE[o['pay_interface_type_code']]]
	# 	o['status'] = mall_models.STATUS2TEXT[mall_models.MEANINGFUL_WORD2ORDER_STATUS[o['status_code']]]
	# 	o['invoice'] = o['bill']
	# 	o['is_group_buying'] = o['is_group_buy']
	# 	o['ship_area'] = o['ship_area_text']
	# 	o['buyer'] = o['member_info']['name']
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)



@when(u"{user}支付订单'{bid}'")
def step_impl(context, user, bid):
	data = {
		"corp_id": context.corp.id,
		"id": get_order_id_by_bid(bid)
	}
	response = context.client.put('/order/paid_order/', data)

	bdd_util.assert_api_call_success(response)

@when(u"{user}取消订单'{bid}'")
def step_impl(context, user, bid):
	data = {
		"corp_id": context.corp.id,
		"id": get_order_id_by_bid(bid)
	}
	response = context.client.put('/order/cancelled_order/', data)
	bdd_util.assert_api_call_success(response)