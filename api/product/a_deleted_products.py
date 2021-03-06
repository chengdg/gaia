# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo


class ADeletedProducts(api_resource.ApiResource):
	"""
	已删除商品集合
	"""
	app = "product"
	resource = "deleted_products"

	@param_required(['corp_id', 'product_ids'])
	def put(args):
		corp = args['corp']
		product_ids = json.loads(args['product_ids'])
		corp.product_pool.delete_verified_products(product_ids)

		return {}