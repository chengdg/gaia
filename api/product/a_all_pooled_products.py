# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.mall.corporation_factory import CorporationFactory
from business.product.encode_product_service import EncodeProductService

class AAllPooledProducts(api_resource.ApiResource):
	"""
	商品池中商品集合
	"""
	app = "product"
	resource = "all_pooled_products"

	@param_required(['corp_id', '?fill_options:json', 'product_ids:json'])
	def get(args):
		corp = args['corp']

		fill_options = {
			'with_product_model': True,
			'with_model_property_info': True,
			'with_cps_promotion_info': True
		} if not args.get('fill_options') else args['fill_options']

		products = corp.product_pool.get_all_products(fill_options, args.get('product_ids'))

		encode_product_service = EncodeProductService.get(corp)
		datas = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			models_info = encode_product_service.get_models_info(product)
			gross_profit_info = encode_product_service.get_gross_profit_info(product)
			cps_promotion_info = encode_product_service.get_cps_promotion_info(product)

			data = {
				"id": product.id,
				"name": base_info['name'],
				"models_info": models_info,
				"created_at": base_info['created_at'],
				'gross_profit_info': gross_profit_info,
				"cps_promotion_info": cps_promotion_info
			}

			datas.append(data)

		return datas
		