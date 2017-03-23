# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.global_product_repository import GlobalProductRepository

class APendingProduct(api_resource.ApiResource):
	"""
	待审核商品
	"""

	app = "product"
	resource = "pending_product"

	@param_required(['corp_id', 'product_id:int'])
	def put(args):
		product_id = args['product_id']
		corp = args['corp']

		product = corp.product_pool.get_product_by_id(product_id)
		product.submit_verify()

		return {}

	@param_required(['corp_id', 'product_ids:json', 'reason'])
	def delete(args):
		product_ids = args['product_ids']
		reason = args['reason']
		corp = args['corp']
		
		for product_id in product_ids:
			product = corp.global_product_repository.get_product(product_id)
			product.refuse_verify(reason)

		return {}