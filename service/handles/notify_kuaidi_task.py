# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""
import time

from eaglet.core.sendmail import sendmail

from business.mall.express.express_service import ExpressService


from business.mall.corporation import Corporation
from service.handler_register import register
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


@register("notify_kuadi_task")
def process(data, recv_msg=None):
	corp_id = data['corp_id']
	delivery_item_id = data['delivery_item_id']

	corp = Corporation(corp_id)

	delivery_item = corp.delivery_item_repository.get_delivery_item(delivery_item_id)
	if delivery_item.with_logistics_trace:
		# 发送快递订阅
		is_success = ExpressService(delivery_item).get_express_poll()
		if not is_success:
			raise Exception(u'快递订阅异常')