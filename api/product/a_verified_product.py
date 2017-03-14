# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AVerifiedProduct(api_resource.ApiResource):

	app = "product"
	resource = "verified_product"

	@param_required(['corp_id', 'product_ids:json'])
	def put(args):
		"""
		入库审核
		"""
		corp = args['corp']
		product_ids = args['product_ids']

		products = corp.global_product_repository.get_products_by_ids(product_ids)
		for product in products:
			product.verify(args['corp'])

		return {}

	@param_required(['corp_id', 'product_ids:json'])
	def post(args):
		"""
		编辑审核
		"""
		corp = args['corp']
		product_ids = args['product_ids']
		products = corp.global_product_repository.get_products_by_ids(product_ids)
		for product in products:
			product.verify_modifications()

		return {}