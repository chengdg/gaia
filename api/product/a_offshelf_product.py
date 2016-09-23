# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf


class AOffshelfProduct(api_resource.ApiResource):
	"""
	待售商品
	"""
	app = "product"
	resource = "offshelf_product"

	@param_required(['corp'])
	def put(args):
		'''
		待售商品列表
		'''
		corp = args['corp']
		corp.forsale_shelf.move_products([args['product_id']])

		return {}