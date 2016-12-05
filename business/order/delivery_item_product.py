# -*- coding: utf-8 -*-
"""@package business.mall.order_products
订单商品(OrderPdocut)集合

OrderProducts用于构建一组OrderProduct，OrderProducts存在的目的是为了后续优化，以最少的数据库访问次数对商品信息进行批量填充

"""

import json

from eaglet.decorator import param_required

from business.product.product import Product
from db.mall import models as mall_models
from eaglet.core import watchdog
from business import model as business_model


class DeliveryItemProduct(business_model.Model):
	"""
	出货单中的商品
	"""
	__slots__ = (
		'id',
		'name',
		'origin_price',  # 下单时的原价
		'sale_price',  # 售价
		'show_sale_price',  # 商品的显示售价，通常和售价一致，只有赠品时，售价为0，而显示商品价格
		'count',
		'weight',
		'delivery_item_id',
		'thumbnails_url',
		'is_deleted',
		'total_origin_price',
		'promotion_info',
		'product_model_name_texts',
		'product_model_name'

	)

# @staticmethod
# @param_required(['corp', 'product_info'])
# def get(args):
# 	product_info = args['product_info']
# 	corp = args['corp']
# 	db_model = product_info['db_model']
#
# 	delivery_item_product = DeliveryItemProduct()
#
# 	delivery_item_product.name = db_model.name
# 	delivery_item_product.id = product_info['id']
# 	delivery_item_product.origin_price = product_info['total_price'] / product_info['number']
# 	delivery_item_product.sale_price = product_info['price']
# 	delivery_item_product.total_origin_price = product_info['total_price']
# 	delivery_item_product.count = product_info['number']
# 	delivery_item_product.delivery_item_id = product_info
# 	# delivery_item_product.product_model_name = 'todo'  # todo
# 	delivery_item_product.product_model_names = 'todo'  # todo
#
# 	delivery_item_product.thumbnails_url = product.thumbnails_url
# 	delivery_item_product.is_deleted = product.is_deleted
#
# 	delivery_item_product.promotion_result = promotion_result
