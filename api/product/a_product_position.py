# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService


class AProductPosition(api_resource.ApiResource):
	"""
	商品排序位置
	"""
	app = "product"
	resource = "product_position"

	@param_required(['corp_id', 'id', 'position'])
	def post(args):
		product_id = args['id']

		update_product_service = UpdateProductService.get(args['corp'])
		update_product_service.update_product_position(product_id, args['position'])

		return {}