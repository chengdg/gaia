# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from business.mall.corporation import Corporation
from business.order.service.paid_order_handle_service import PaidOrderHandleService
from service.service_register import register


@register("order_paid")
def order_process(data, recv_msg=None):
	"""
	演示接收消息
	"""

	corp_id = data['corp_id']
	order_id = data['order_id']
	order_bid = data['order_bid']

	corp = Corporation(corp_id)

	service = PaidOrderHandleService.get(corp)
	try:
		service.handle(order_id)
	except BaseException as e:
		from eaglet.core.exceptionutil import unicode_full_stack
		print('_______-')
		print(unicode_full_stack())
		print('_______-')
		raise e
