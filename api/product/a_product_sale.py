# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService


class AProductStock(api_resource.ApiResource):
	"""
	商品库存
	"""
	app = "product"
	resource = "product_sale"

	@param_required(['corp', 'id', 'changed_count'])
	def post(args):
		product_id = args['id']
		changed_count = args['changed_count']

		update_product_service = UpdateProductService.get(args['corp'])
		update_product_service.update_product_sale(product_id, changed_count)

		return {}