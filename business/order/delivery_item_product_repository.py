# -*- coding: utf-8 -*-
"""@package business.mall.order_products
订单商品(OrderPdocut)集合

OrderProducts用于构建一组OrderProduct，OrderProducts存在的目的是为了后续优化，以最少的数据库访问次数对商品信息进行批量填充

"""

import json

from eaglet.decorator import param_required

from business.order.delivery_item_product import DeliveryItemProduct
from db.mall import models as mall_models
from business import model as business_model


class DeliveryItemProductRepository(business_model.Model):
	# __slots__ = (
	# 	'corp'
	# )

	def __init__(self, corp):

		business_model.Model.__init__(self)

		self.corp = corp

	@staticmethod
	@param_required(['corp'])
	def get(args):
		corp = args['corp']

		return DeliveryItemProductRepository(corp)

	def get_products_for_delivery_items(self, delivery_items, with_premium_sale):
		delivery_item_ids = [delivery_item.id for delivery_item in delivery_items]
		ohp_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=delivery_item_ids)
		product_ids = [p.product_id for p in ohp_list]

		products = self.corp.product_pool.get_products_by_ids(product_ids, {"with_product_model": True,"with_property":True})
		product_id2product = {p.id: p for p in products}


		origin_order_ids = [delivery_item.origin_order_id for delivery_item in delivery_items]
		id2promotion = {r.promotion_id: r for r in
		                mall_models.OrderHasPromotion.select().dj_where(order_id__in=origin_order_ids)}

		delivery_item_products = []
		for r in ohp_list:
			product = product_id2product[r.product_id]

			promotion = id2promotion.get(r.promotion_id, None)
			if promotion:
				promotion_result = json.loads(promotion.promotion_result_json)
				promotion_result['type'] = promotion.promotion_type
			else:
				promotion_result = None

			delivery_item_product = DeliveryItemProduct()
			delivery_item_product.name = product.name
			delivery_item_product.id = r.product_id
			delivery_item_product.origin_price = r.total_price / r.number
			delivery_item_product.sale_price = r.price
			delivery_item_product.total_origin_price = r.total_price
			delivery_item_product.count = r.number
			delivery_item_product.product_model_name = r.product_model_name
			delivery_item_product.delivery_item_id = r.order_id

			if r.product_model_name == 'standard':
				delivery_item_product.product_model_names = []
			else:
				delivery_item_product.product_model_names = ['todo1', 'todo2']
			delivery_item_product.thumbnails_url = product.thumbnails_url
			delivery_item_product.is_deleted = product.is_deleted

			delivery_item_product.promotion_result = promotion_result

			# delivery_item_product_info = {
			# 	'rid': r.id,
			# 	'id': r.product_id,
			# 	'model_name': r.product_model_name,
			# 	'count': r.number,
			# 	'promotion_id': r.promotion_id,
			# 	'price': r.price,
			# 	'total_price': r.total_price,
			# 	'promotion_money': r.promotion_money,
			# 	'discount_money': r.grade_discounted_money,
			# 	'promotion_result': promotion_result,
			# 	'integral_sale_id': r.integral_sale_id,
			# 	'delivery_item_id': r.order_id,
			# 	'db_model': product_db_model
			# }
			#
			# delivery_item_product = DeliveryItemProduct.get({
			# 	'corp': self.corp,
			# 	'product_info': delivery_item_product_info
			# })

			delivery_item_products.append(delivery_item_product)

		return delivery_item_products
