# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory


class AProduct(api_resource.ApiResource):
	"""
	商品
	"""
	app = "product"
	resource = "product"

	@param_required(['base_info', 'models_info', 'image_info', 'postage_info', 'pay_info', 'categories', 'properties'])
	def put(args):
		"""
		创建商品
		@return:
		"""
		product_data = args
		product_factory = ProductFactory.get(args['corp'])
		product_factory.create_product(product_data)

		return {}

	@param_required([])
	def post(args):
		product_factory = ProductFactory.get()
		product_factory.update_product(args['id'], args)

		return {}

	@param_required(['ids'])
	def delete(args):
		pids = args['ids'].split(',')
