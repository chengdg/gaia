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
		'count',
		'delivery_item_id',
		'thumbnails_url',
		'is_deleted',
		'total_origin_price',
		'promotion_result',
		'product_model_name'

	)
