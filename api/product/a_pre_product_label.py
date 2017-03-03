# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.global_product_repository import GlobalProductRepository
from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService


class APreProduct(api_resource.ApiResource):
	"""
	原始商品标签
	"""
	app = "product"
	resource = "pre_product_label"

	@param_required(['corp_id', 'product_id:int', 'label_ids:json'])
	def put(args):
		product_id = args.get('product_id')

		return {}

		