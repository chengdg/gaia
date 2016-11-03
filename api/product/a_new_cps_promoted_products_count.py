# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory


class ANewCPSPromotedProductsCount(api_resource.ApiResource):
	"""
	cps推广商品新增数量
	"""
	app = 'product'
	resource = 'new_cps_promoted_products_count'

	@param_required(['corp_id', 'product_status'])
	def get(args):
		"""
		product_status 推广的销售状态 insale:销售, forsale:待售, pool: 商品池

		"""
		corp = args['corp']
		product_status = args['product_status']
		if product_status == 'insale':
			count = corp.insale_shelf.get_new_promoted_products_count()
		elif product_status == 'forsale':
			count = corp.forsale_shelf.get_new_promoted_products_count()
		else:
			count = corp.product_pool.get_new_promoted_products_count()
		return {
			'count': count
		}

	@param_required(['corp_id', 'product_status'])
	def post(args):
		"""
		product_status 推广的销售状态 insale:销售, forsale:待售, pool: 商品池

		"""
		corp = args['corp']
		product_status = args['product_status']
		if product_status == 'insale':
			corp.insale_shelf.update_new_promoted_products_count()
		elif product_status == 'forsale':
			corp.forsale_shelf.update_new_promoted_products_count()
		else:
			corp.product_pool.update_new_promoted_products_count()
		return {}
