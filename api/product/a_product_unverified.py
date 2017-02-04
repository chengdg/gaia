# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_classification.product_classification_repository import ProductClassificationRepository
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

		product_unverified_data = GlobalProductRepository.get().get_product_unverified(product_id)

		base_info = product_unverified_data['base_info']
		models_info = product_unverified_data['models_info']
		image_info = product_unverified_data['image_info']
		logistics_info = product_unverified_data['logistics_info']

		return {
			'name': base_info['name'],
			'promotion_title': base_info['promotion_title'],
			'price_info': {
				'display_price':base_info['price']
			},
			'weight': models_info['standard_model']['weight'],
			'stocks': models_info['standard_model']['stocks'],
			'detail': base_info['detail'],
			'models': models_info['custom_models'],
			'images': image_info['images'],
			'limit_zone_type': logistics_info['limit_zone_type'],
			'limit_zone': logistics_info['limit_zone_id'],
			'postage_money': logistics_info['unified_postage_money'],
			'classification_id': base_info['classification_id'],
			'classification_name_nav': ProductClassificationRepository.get().get_product_classification(base_info['classification_id']).get_nav()
		}

	@param_required(['corp_id', 'product_id', 'base_info:json', 'models_info:json', 'image_info:json', 'logistics_info:json'])
	def put(args):
		product_id = args.get('product_id')

		product = GlobalProductRepository.get().get_product(product_id)

		product.update_product_unverified(args)

		return {}

		