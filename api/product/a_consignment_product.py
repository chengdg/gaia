# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory

class AConsignmentProduct(api_resource.ApiResource):
	"""
	代售商品：从微众商品池中选择的，由自营平台代售的商品
	"""
	app = "product"
	resource = "consignment_product"

	@param_required(['corp_id', 'product_id'])
	def put(args):
		corp = args['corp']
		product_ids = [args['product_id']]
		corp.product_pool.add_consignment_products(product_ids)

		return {}
