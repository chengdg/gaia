# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AProcessedCPSPromotedProducts(api_resource.ApiResource):
	"""
	自营平台处理cps推广商品
	"""
	app = 'product'
	resource = 'processed_cps_promoted_products'

	@param_required(['corp_id', 'product_ids'])
	def put(args):
		"""
		product_ids [product_id, ......]
		"""
		corp = args['corp']
		product_ids = args['product_ids']
		product_ids = json.loads(product_ids)
		corp.product_pool.set_cps_promoted_products_processed(product_ids)
		return {}
