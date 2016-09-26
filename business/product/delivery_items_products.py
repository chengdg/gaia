# -*- coding: utf-8 -*-
"""@package business.mall.order_products
订单商品(OrderPdocut)集合

OrderProducts用于构建一组OrderProduct，OrderProducts存在的目的是为了后续优化，以最少的数据库访问次数对商品信息进行批量填充

"""

import json

from eaglet.decorator import param_required

from db.mall import models as mall_models
from eaglet.core import watchdog
from business import model as business_model


class DeliveryItemProduct(business_model.Model):
	__slots__ = (
		'id',
		'name',
		'origin_price',  # 下单时的原价
		'sale_price',  # 售价
		'count',
		'delivery_item_id',
		'thumbnails_url',
		'is_deleted',
		'total_origin_price',
		'promotion_result'

	)


class DeliveryItemsProducts(business_model.Model):
	"""订单商品集合
	"""
	__slots__ = (
		'products',
	)

	@staticmethod
	def get_for_delivery_items(delivery_items, with_premium_sale):
		# type: list(Order) -> object
		delivery_item_ids = [delivery_item.id for delivery_item in delivery_items]
		ohp_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=delivery_item_ids)

		product_ids = [p.product_id for p in ohp_list]
		product_db_models = mall_models.Product.select().dj_where(id__in=product_ids)

		product_id2product = {p.id: p for p in product_db_models}

		origin_order_ids = [delivery_item.origin_order_id for delivery_item in delivery_items]
		id2promotion = {r.promotion_id: r for r in mall_models.OrderHasPromotion.select().dj_where(order_id__in=origin_order_ids)}

		delivery_item_products = []
		for ohs in ohp_list:
			product_db_model = product_id2product[ohs.product_id]

			promotion = id2promotion.get(ohs.promotion_id, None)
			if promotion:
				promotion_result = json.loads(promotion.promotion_result_json)
				promotion_result['type'] = promotion.promotion_type
			else:
				promotion_result = None

			delivery_item_product = DeliveryItemProduct()
			delivery_item_product.name = product_db_model.name
			delivery_item_product.id = ohs.product_id
			delivery_item_product.origin_price = ohs.total_price / ohs.number
			delivery_item_product.sale_price = ohs.price
			delivery_item_product.total_origin_price = ohs.total_price
			delivery_item_product.count = ohs.number
			delivery_item_product.delivery_item_id = ohs.order_id

			delivery_item_product.thumbnails_url = product_db_model.thumbnails_url
			delivery_item_product.is_deleted = product_db_model.is_deleted

			delivery_item_product.promotion_result = promotion_result

			delivery_item_products.append(delivery_item_product)

		return delivery_item_products
