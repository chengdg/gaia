# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""

from eaglet.core import watchdog

from business import model as business_model
from db.mall import models as mall_models


class PaidOrderHandleService(business_model.Service):
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

