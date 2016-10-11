# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService


class AProductPrice(api_resource.ApiResource):
	"""
	商品
	"""
	app = "product"
	resource = "product_price"

	@param_required(['corp_id', 'id', 'price_infos'])
	def post(args):
		product_id = args['id']
		price_infos = json.loads(args['price_infos'])

		update_product_service = UpdateProductService.get(args['corp'])
		update_product_service.update_product_price(product_id, price_infos)

		return {}