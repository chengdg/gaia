# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory


class AProcessedCPSPromotedProducts(api_resource.ApiResource):
	"""
	自营平台处理过的新增cps推广商品的数量
	"""
	app = 'product'
	resource = 'processed_cps_promoted_products'

	@param_required(['corp_id', 'product_status'])
	def put(args):
		"""
		product_status 推广的销售状态 insale:销售, forsale:待售, pool: 商品池
		"""
		corp = args['corp']
		product_status = args['product_status']
		if product_status == 'insale':
			corp.insale_shelf.set_cps_promoted_products_processed()
		elif product_status == 'forsale':
			corp.forsale_shelf.set_cps_promoted_products_processed()
		else:
			corp.product_pool.set_cps_promoted_products_processed()
		return {}
