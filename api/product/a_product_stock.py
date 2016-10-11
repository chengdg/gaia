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
	resource = "product_stock"

	@param_required(['corp_id', 'id', 'stock_infos'])
	def post(args):
		product_id = args['id']
		stock_infos = json.loads(args['stock_infos'])

		update_product_service = UpdateProductService.get(args['corp'])
		update_product_service.update_product_stock(product_id, stock_infos)

		return {}