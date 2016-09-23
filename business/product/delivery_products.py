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
# from business.product.order_product import OrderProduct

import settings


class DeliveryItemProduct(business_model.Model):

	__slots__ = (
		'id',
		'name',
		'price',
		'count',
		'delivery_item_id'

	)


class DeliveryItemsProducts(business_model.Model):
	"""订单商品集合
	"""
	__slots__ = (
		'products',
	)

	@staticmethod
	def get_for_delivery_items(delivery_items):
		# type: list(Order) -> object
		delivery_item_ids = [delivery_item.id for delivery_item in delivery_items]
		ohs_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=delivery_item_ids)

		product_ids = [p.id for p in ohs_list]
		product_db_models = mall_models.Product.select().dj_where(id__in=product_ids)

		product_id2product = {p.id: p for p in product_db_models}

		# delivery_item_product.name =

		delivery_item_products = []
		for db_model in ohs_list:
			delivery_item_product = DeliveryItemProduct()
			delivery_item_product.name = db_model.product_name
			delivery_item_product.id = db_model.product_id
			delivery_item_product.price = db_model.total_price / db_model.number
			delivery_item_product.count = db_model.number
			delivery_item_product.delivery_item_id = db_model.order_id

			delivery_item_products.append(delivery_item_product)

		return delivery_item_products
