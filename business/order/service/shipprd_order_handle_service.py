# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""

from eaglet.core import watchdog

from business import model as business_model
from db.mall import models as mall_models
from bdem import msgutil

from zeus_conf import TOPIC


class PaidOrderHandleService(business_model.Service):
	"""
	- 更新商品消息
	- 发送运营通知邮件
	- 发送模板消息
	"""

	def handle(self, order_id):
		fill_options = {
			'with_delivery_items': {
				'with_products': True,
			}

		}
		order = self.corp.order_repository.get_order(order_id, fill_options)



		# 发送运营邮件通知
		topic_name = TOPIC['base_service']
		data = {
			"order_id": order.id,
			"corp_id": self.corp.id
		}
		msgutil.send_message(topic_name, 'send_order_email_task', data)

		# 发送模板消息
		topic_name = TOPIC['base_service']
		data = {
			"order_id": order.id,
			"corp_id": self.corp.id
		}
		msgutil.send_message(topic_name, 'send_template_message_task', data)
