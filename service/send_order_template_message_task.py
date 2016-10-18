# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""
import time

from eaglet.core.sendmail import sendmail

import settings
from business.mall.notify.notification_repository import NotificationRepository
from service.service_register import register

# -*- coding: utf-8 -*-
from util.regional_util import get_str_value_by_string_ids

"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from business.mall.corporation import Corporation
from business.order.service.paid_order_handle_service import PaidOrderHandleService
from service.service_register import register
from db.mall import models as mall_models

ORDER_STATUS2NOTIFY_STATUS = {
	mall_models.ORDER_STATUS_NOT: mall_models.PLACE_ORDER,
	mall_models.ORDER_STATUS_PAYED_NOT_SHIP: mall_models.PAY_ORDER,
	mall_models.ORDER_STATUS_PAYED_SHIPED: mall_models.SHIP_ORDER,
	mall_models.ORDER_STATUS_SUCCESSED: mall_models.SUCCESSED_ORDER,
	mall_models.ORDER_STATUS_CANCEL: mall_models.CANCEL_ORDER
}


def __send_email(emails, content_described, content):
	for email in emails:
		sendmail(email, content_described, content)


@register("send_order_template_task")
def process(data, recv_msg=None):
	corp_id = data['corp_id']
	order_id = data['order_id']

	corp = Corporation(corp_id)

	fill_options = {
		'with_member': True,
		'with_delivery_items': {
			'with_products': True,

		}

	}
	order = corp.order_repository.get_order(order_id, fill_options)
	# 更新商品销量
	delivery_item_products = []
	for item in order.delivery_items:
		delivery_item_products.extend(item.products)

	notification_repository = NotificationRepository.get(corp)
	order_notify_type = ORDER_STATUS2NOTIFY_STATUS.get(order.status, -1)
	order_notify = notification_repository.get_email_notification_by_type(order_notify_type)

	pass
