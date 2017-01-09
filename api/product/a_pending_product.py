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

		product = GlobalProductRepository.get().get_product(product_id)
		product.submit_verify()

		return {}

	@param_required(['corp_id', 'product_id:int', 'reason'])
	def delete(args):
		product_id = args['product_id']
		reason = args['reason']

		product = GlobalProductRepository.get().get_product(product_id)
		product.refuse_verify(reason)

		return {}