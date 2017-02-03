# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.global_product_repository import GlobalProductRepository

class AProductUnverified(api_resource.ApiResource):
	"""
	未审核的商品信息
	"""
	app = "product"
	resource = "product_unverified"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		product_id = args.get('product_id')

		product_unverified = GlobalProductRepository.get().get_product_unverified(product_id)

		return {
			'name': product_unverified.get('name'),
			'promotion_title': product_unverified.get('promotion_title'),
			'price_info': product_unverified.get('price_info'),
			'weight': '0.00' if product_unverified.get('models') else product_unverified.get('weight', '0.00'),
			'stocks': product_unverified.get('stocks'),
			'detail': product_unverified.get('detail'),
			'models': product_unverified.get('models'),
			'images': product_unverified.get('images'),
			'limit_zone_type': product_unverified.get('limit_zone_type'),
			'limit_zone': product_unverified.get('limit_zone'),
			'postage_money': '%.2f' % product_unverified.get('unified_postage_money', 0.00),
			'classification_id': product_unverified.get('classification_id'),
			'classification_name_nav': product_unverified.get('classification_nav')
		}

	@param_required(['corp_id', 'product_id', 'base_info:json', 'models_info:json', 'image_info:json', 'logistics_info:json'])
	def put(args):
		product_id = args.get('product_id')

		product = GlobalProductRepository.get().get_product(product_id)

		product.update_product_unverified(args)

		return {}

		