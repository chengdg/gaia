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

	@param_required(['corp_id'])
	def get(args):
		"""

		"""
		corp = args['corp']

		count = corp.product_pool.unprocessed_cps_promoted_products_count()
		return {
			'count': count
		}
