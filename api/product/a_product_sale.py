# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService


class AProductPrice(api_resource.ApiResource):
	"""
	商品
	"""
	app = "product"
	resource = "product_sale"

	@param_required(['corp_id', 'id', 'count'])
	def post(args):
		product_id = args['id']
		corp = args['corp']

		prodcut = corp.product_pool.get_products_by_ids([product_id])[0]
		prodcut.update_sales(args['count'])

		return {}