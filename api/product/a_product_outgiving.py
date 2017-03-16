# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory


class AProductOutgiving(api_resource.ApiResource):
	"""
	分发商品到社群
	"""
	app = "product"
	resource = "product_outgiving"

	@param_required(['corp_id', 'product_ids:json'])
	def put(args):
		product_factory = ProductFactory.get(args['corp'])
		product_factory.outgiving_products(args['product_ids'])

		return {}
