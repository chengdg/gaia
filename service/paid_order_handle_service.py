# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from business.mall.corporation import Corporation
from service.service_register import register
from db.mall import models as mall_models


@register("pay_order")
def order_process(data, recv_msg=None):
	"""
	演示接收消息
	"""

	corp_id = data['corp_id']
	order_id = data['order_id']
	order_bid = data['order_bid']

	corp = Corporation(corp_id)

	fill_options = {
		'with_delivery_items': {
			'with_products': True,
		}

	}
	order = corp.order_repository.get_order(order_id, fill_options)

	products = []
	for item in order.delivery_items:
		products.extend(item.products)
	# todo 赠品不计销量
	# for product in products:
	# 	if product.promotion != {'type_name': 'premium_sale:premium_product'}:
	# 		product_sale_infos.append({
	# 			'product_id': product.id,
	# 			'purchase_count': product.purchase_count
	# 		})
	for product in products:
		if mall_models.ProductSales.select().dj_where(product_id=product.id).first():
			mall_models.ProductSales.update(
				sales=mall_models.ProductSales.sales + product.count).dj_where(product_id=product.id).execute()
		else:
			mall_models.ProductSales.create(product=product.id, sales=product.count)
