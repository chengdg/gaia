# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo

from business.product.encode_product_service import EncodeProductService

class ASpecificIdProducts(api_resource.ApiResource):
	"""
	指定id的商品集合
	"""
	app = "product"
	resource = "specific_id_products"

	@param_required(['corp_id', 'ids:json', 'fill_options:json'])
	def get(args):
		corp = args['corp']

		fill_options = args['fill_options']
		has_product_model_info = 'with_product_model' in fill_options

		fill_options = {
			'with_category': True,
			'with_product_model': True
		}

		products = corp.product_pool.get_products_by_ids(args['ids'], fill_options)

		encode_product_service = EncodeProductService.get(corp)
		datas = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			
			data = {
				"id": product.id,
				"name": base_info['name'],
				"create_type": base_info['create_type'],
				"is_member_product": base_info['is_member_product'],
				"bar_code": base_info['bar_code'],
				"display_index": base_info['display_index'],
				"created_at": base_info['created_at']
			}

			if has_product_model_info:
				data['models_info'] = encode_product_service.get_models_info(product)

			datas.append(data)

		return {
			'products': datas
		}