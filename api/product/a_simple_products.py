# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.product.encode_product_service import EncodeProductService


class ASimpleProducts(api_resource.ApiResource):
	"""
	简单商品
	名字,首图,价格,id
	
	"""
	app = "product"
	resource = "simple_products"

	@param_required(['corp_id', 'product_ids'])
	def get(args):
		corp = args['corp']
		product_ids = args.get('product_ids', '[]')
		product_ids = json.loads(product_ids)
			
		products = corp.insale_shelf.get_simple_products(product_ids)
		encode_product_service = EncodeProductService.get(corp)
		data = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			models_info = encode_product_service.get_models_info(product)
			image_info = encode_product_service.get_image_info(product)
			data.append({
				"id": product.id,
				"name": base_info['name'],
				"models_info": models_info,
				'image_info': image_info,
			})

		return {
			'products': data
		}
