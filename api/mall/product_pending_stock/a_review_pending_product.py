# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class APendingProduct(api_resource.ApiResource):
	"""
	审核商品
	"""
	app = "mall"
	resource = "review_pending_product"

	@param_required(['corp_id', 'product_ids:json'])
	def put(args):
		"""
		审核通过
		"""
		corp = args['corp']
		product_ids = args['product_ids']

		corp.pending_stock_product_repository.review_accept(product_ids)
		return {}

	@param_required(['corp_id', 'product_id:int', 'reason'])
	def delete(args):
		"""
		审核不通过(入库审核，修改审核)
		"""
		corp = args['corp']
		product_id = args['product_id']
		reason = args['reason']

		corp.pending_stock_product_repository.review_reject(product_id, reason)
		return {}