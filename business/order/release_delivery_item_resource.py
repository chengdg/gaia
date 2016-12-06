# -*- coding: utf-8 -*-
"""


"""
from eaglet.utils.resource_client import Resource

from business import model as business_model
from business.account.integral import Integral
from db.mall import models as mall_models
from db.member import models as member_models


class ReleaseDeliveryItemResourceService(business_model.Service):
	def release(self, delivery_item_id,from_status,to_status):
		"""
		当处理的是出货单时，需要决策是否处理以及如何处理订单
		对于db层面有没有出货单的订单，db操作已经在出货单完成，只用发送消息通知
		@param delivery_item_id:
		@param from_status:
		@param to_status:
		@return:
		"""

		fill_options = {
			'with_products': True

		}
		corp = self.corp
		delivery_item = corp.delivery_item_repository.get_delivery_item(delivery_item_id, fill_options)

		if delivery_item.has_db_redcord:
			is_paid = (mall_models.MEANINGFUL_WORD2ORDER_STATUS[from_status] != mall_models.ORDER_STATUS_NOT)  # 已经支付过的订单，已增加过销量

			delivery_item_products = delivery_item.products
			product_ids = [p.id for p in delivery_item_products]
			product_id2delivery_item_product = {p.id: p for p in delivery_item_products}

			products = corp.product_pool.get_products_by_ids(product_ids)
			#
			# for delivery_item_product in delivery_item_products:
			# 	product = corp.product_pool.get_products_by_ids([delivery_item_product.id])[0]
			#
			# 	product.update_sales(delivery_item_product.count)

			for product in products:
				delivery_item_product = product_id2delivery_item_product[product.id]

				# 更新销量库存
				product.update_stock(delivery_item_product.product_model_name, delivery_item_product.count)

				# 更新销量,赠品不算销量
				if is_paid and delivery_item_product.promotion_info['type'] != "premium_sale:premium_product":
					product.update_sales(0 - delivery_item_product.count)
