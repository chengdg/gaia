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
		# 更新商品销量
		product_infos = []
		for item in order.delivery_items:
			product_infos.extend(item.products)
		# todo 赠品不计销量
		# for product in products:
		# 	if product.promotion != {'type_name': 'premium_sale:premium_product'}:
		# 		product_sale_infos.append({
		# 			'product_id': product.id,
		# 			'purchase_count': product.purchase_count
		# 		})
		for product_info in product_infos:
			product = self.corp.product_pool.get_products_by_ids([product_info.id])[0]

			product.update_sales(product_info.count)

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
