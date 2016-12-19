# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AProducts(api_resource.ApiResource):
	"""
	商品集合
	"""
	app = "mall"
	resource = "product_preview_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		preview_products = corp.product_preview_repository.get_products()

		return {
			'can_created': True,
			'user_has_products': len(preview_products)
		}
		