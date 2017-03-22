# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required


class AProductCustomizePrice(api_resource.ApiResource):
	"""
	商品改价
	"""
	app = "product"
	resource = "product_customize_price"

	@param_required(['corp_id', 'product_id:int', 'customized_models:json'])
	def post(args):
		corp = args['corp']
		product = corp.product_pool.get_product_by_id(args['product_id'])
		print args['customized_models']
		for product_model_id, price in args['customized_models'].items():
			product.customize_price(float(price), int(product_model_id))

		return {}
