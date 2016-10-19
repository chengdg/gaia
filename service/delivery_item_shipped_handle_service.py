# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from business.mall.corporation import Corporation
from business.mall.express.express_service import ExpressService
from business.mall.express.kdniao_express_poll import KdniaoExpressPoll
from business.order.service.paid_order_handle_service import PaidOrderHandleService
from service.service_register import register
from db.express import models as express_models


@register("delivery_item_shipped")
def process(data, recv_msg=None):
	"""
	演示接收消息
	"""

	corp_id = data['corp_id']
	delivery_item_id = data['delivery_item_id']

	corp = Corporation(corp_id)

	try:
		delivery_item = corp.delivery_item_repository.get_delivery_item(delivery_item_id)
		if delivery_item.with_logistics_trace:

			# 发送快递订阅
			ExpressService(delivery_item).get_express_poll()
	except BaseException as e:
		from eaglet.core.exceptionutil import unicode_full_stack
		print(unicode_full_stack())
		raise e