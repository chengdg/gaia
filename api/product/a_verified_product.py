# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.global_product_repository import GlobalProductRepository

class AVerifiedProduct(api_resource.ApiResource):

	app = "product"
	resource = "verified_product"

	@param_required(['corp_id', 'product_ids:json'])
	def put(args):
		product_ids = args['product_ids']

		products = GlobalProductRepository.get().get_products_by_ids(product_ids)
		for product in products:
			product.verify(args['corp'])

		return {}