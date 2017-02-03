# -*- coding:utf-8 -*-

import types
import json

from behave import *

from business.mall.logistics.express_delivery_repository import COMPANIES
from features.util import bdd_util
from db.mall import models as mall_models


def get_id_by_bid(bid):
	return mall_models.Order.select().dj_where(order_id=bid).first().id


def get_delivery_item_bid(bid):
	if "^" in bid:
		supplier_name = bid.split("^")[1]
		supplier_id = mall_models.Supplier.select().dj_where(name=supplier_name).first().id

		return bid.split("^")[0] + "^" + str(supplier_id) + "s"

	elif "-" in bid:
		supplier_name = bid.split("-")[1]
		supplier_id = mall_models.Supplier.select().dj_where(name=supplier_name).first().id

		return bid.split("-")[0] + "^" + str(supplier_id) + "s"
	else:
		return bid


def get_supplier_name_by_id(id):
	return mall_models.Supplier.select().dj_where(id=id).first().name


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


	for order in actual:

		if order['extra_coupon_info']['type'] == 'all_products_coupon':
			order['extra_coupon_info']['type'] = u'通用券'
		elif order['extra_coupon_info']['type'] == 'multi_products_coupon':
			order['extra_coupon_info']['type'] = u'多商品券'

		for delivery_item in order['delivery_items']:
			real_bid = delivery_item['bid']
			if "^" in real_bid:
				x_bid = real_bid.split("^")[0] + '-' + str(
					get_supplier_name_by_id(real_bid.split("^")[1].replace("s", "")))
				delivery_item['bid'] = x_bid
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


def __alert_order_action_time(bid, payment_time, to_status, action):
	mall_models.Order.update(payment_time=payment_time).dj_where(order_id__icontains=bid).execute()
	mall_models.OrderOperationLog.update(created_at=payment_time).dj_where(order_id__icontains=bid,
	                                                                       action__icontains=action).execute()
	mall_models.OrderStatusLog.update(created_at=payment_time).dj_where(order_id__icontains=bid,
	                                                                    to_status=to_status).execute()


@when(u"{user}支付订单'{bid}'")
def step_impl(context, user, bid):
	data = {
		"corp_id": context.corp.id,
		"id": get_id_by_bid(bid)
	}

	response = context.client.put('/order/paid_order/', data)
	try:
		payment_time = json.loads(context.text)['time']
		__alert_order_action_time(bid, payment_time, mall_models.ORDER_STATUS_PAYED_NOT_SHIP, u'支付')
	except BaseException as e:

		pass
	bdd_util.assert_api_call_success(response)


@when(u"{user}取消订单'{bid}'")
def step_impl(context, user, bid):
	data = {
		"corp_id": context.corp.id,
		"id": get_id_by_bid(bid)
	}
	response = context.client.put('/order/cancelled_order/', data)
	bdd_util.assert_api_call_success(response)


for company in COMPANIES:
	company['unicode_name'] = company['name'].decode('utf-8')


def __get_express_company_name_value_by_name(name):
	for company in COMPANIES:
		if name == company['unicode_name']:
			return company['value']

	return ''


@when(u"{user}对出货单进行发货")
def step_impl(context, user):
	ship_infos = json.loads(context.text)

	for ship_info in ship_infos:
		ship_info['delivery_item_bid'] = get_delivery_item_bid(ship_info['delivery_item_bid'])
		if ship_info['with_logistics_trace']:
			ship_info['express_company_name_value'] = __get_express_company_name_value_by_name(
				ship_info['express_company_name_value'])

	data = {
		"corp_id": context.corp.id,
		"ship_infos": json.dumps(ship_infos)
	}
	response = context.client.put('/order/shipped_delivery_items/', data)
	bdd_util.print_json(response.body['data'])
	bdd_util.assert_api_call_success(response)


@when(u"{user}修改出货单'{bid}'物流信息")
def step_impl(context, user, bid):
	bid = get_delivery_item_bid(bid)
	delivery_item_id = get_id_by_bid(bid)
	ship_info = json.loads(context.text)
	if ship_info['with_logistics_trace']:
		ship_info['express_company_name_value'] = __get_express_company_name_value_by_name(
			ship_info['express_company_name_value'])

	data = {
		"corp_id": context.corp.id,
		"delivery_item_id": delivery_item_id,
		"new_ship_info": json.dumps(ship_info)
	}
	response = context.client.post('/order/delivery_item/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}给订单添加备注信息")
def step_impl(context, user):
	order_id = get_id_by_bid(json.loads(context.text)['bid'])
	remark = json.loads(context.text)['remark']
	url = '/order/order/?corp_id=%d&id=%d' % (context.corp.id, order_id)
	response = context.client.post(url, data={'new_remark': remark})
	bdd_util.assert_api_call_success(response)


@when(u"{user}标记完成出货单'{bid}'")
def step_impl(context, user, bid):
	bid = get_delivery_item_bid(bid)
	delivery_item_id = get_id_by_bid(bid)
	data = {
		'corp_id': context.corp.id,
		'delivery_item_id': delivery_item_id
	}
	response = context.client.put('/order/finished_delivery_item/', data)
	bdd_util.assert_api_call_success(response)


@then(u"{user}获得订单'{bid}'")
def step_impl(context, user, bid):
	order_id = get_id_by_bid(bid)
	url = '/order/order/?corp_id=%d&id=%d' % (context.corp.id, order_id)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	actual = response.data["order"]
	if actual['extra_coupon_info']['type'] == 'all_products_coupon':
		actual['extra_coupon_info']['type'] = u'通用券'
	elif actual['extra_coupon_info']['type'] == 'multi_products_coupon':
		actual['extra_coupon_info']['type'] = u'多商品券'
	for delivery_item in actual['delivery_items']:
		real_bid = delivery_item['bid']
		if "^" in real_bid:
			x_bid = real_bid.split("^")[0] + '-' + str(
				get_supplier_name_by_id(real_bid.split("^")[1].replace("s", "")))
			delivery_item['bid'] = x_bid
	# 暂时不验证时间

	if actual['integral_type'] == 'order':
		actual['integral_type'] = u'整单抵扣'
	elif actual['integral_type'] == 'product':
		actual['integral_type'] = u'积分应用'

	# for delivey_item
	# for o in actual:
	# 	o['order_no'] = o['bid']
	# 	o['methods_of_payment'] = mall_models.PAYTYPE2NAME[mall_models.PAYSTR2TYPE[o['pay_interface_type_code']]]
	# 	o['status'] = mall_models.STATUS2TEXT[mall_models.MEANINGFUL_WORD2ORDER_STATUS[o['status_code']]]
	# 	o['invoice'] = o['bill']
	# 	o['is_group_buying'] = o['is_group_buy']
	# 	o['ship_area'] = o['ship_area_text']
	# 	o['buyer'] = o['member_info']['name']
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual, ignore_keys=['time'])


@when(u"{user}申请退款出货单'{bid}'")
def step_impl(context, user ,bid):
	"""
	@type context: behave.runner.Context
	"""
	pass