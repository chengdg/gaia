# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

from bdem import msgutil

from business.mall.corporation import Corporation
from service.service_register import register
from zeus_conf import TOPIC


@register("order_paid")
def process(data, recv_msg=None):
	"""
	处理支付订单消息
	"""

	corp_id = data['corp_id']
	order_id = data['order_id']
	order_bid = data['order_bid']
	from_status = data['from_status']
	to_status = data['to_status']

	corp = Corporation(corp_id)

	fill_options = {
		'with_member': True,
		'with_delivery_items': {
			'with_products': True,
		}

	}
	order = corp.order_repository.get_order(order_id, fill_options)
	# 更新商品销量

	# todo 赠品不计销量
	# for product in products:
	# 	if product.promotion != {'type_name': 'premium_sale:premium_product'}:
	# 		product_sale_infos.append({
	# 			'product_id': product.id,
	# 			'purchase_count': product.purchase_count
	# 		})

	delivery_item_products = order.get_all_products()
	for product_info in delivery_item_products:
		product = corp.product_pool.get_products_by_ids([product_info.id])[0]

		product.update_sales(product_info.count)

	# 发送运营邮件通知
	topic_name = TOPIC['base_service']
	data = {
		"type": "order",
		"order_id": order.id,
		"corp_id": corp.id
	}
	msgutil.send_message(topic_name, 'send_order_email_task', data)

	# 发送模板消息
	topic_name = TOPIC['base_service']
	data = {
		"order_id": order.id,
		"corp_id": corp.id
	}
	msgutil.send_message(topic_name, 'send_template_message_task', data)

	order = corp.order_repository.get_order(order_id, fill_options)
	member = corp.member_repository.get_member_by_id(order.member_info['id'])
	member.update_pay_info(order, from_status, to_status)
