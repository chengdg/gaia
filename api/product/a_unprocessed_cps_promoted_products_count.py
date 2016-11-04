# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory


class AUnprocessedCPSPromotedProductsCount(api_resource.ApiResource):
	"""
	自营平台未处理的新增cps推广商品的数量
	"""
	app = 'product'
	resource = 'unprocessed_cps_promoted_products_count'

	@param_required(['corp_id', 'product_status'])
	def get(args):
		"""
		product_status 推广的销售状态 insale:销售, forsale:待售, pool: 商品池

		"""
		corp = args['corp']
		product_status = args['product_status']
		if product_status == 'insale':
			count = corp.insale_shelf.unprocessed_cps_promoted_products_count()
		elif product_status == 'forsale':
			count = corp.forsale_shelf.unprocessed_cps_promoted_products_count()
		else:
			count = corp.product_pool.unprocessed_cps_promoted_products_count()
		return {
			'count': count
		}
