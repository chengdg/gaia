# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_classification.product_classification_repository import ProductClassificationRepository

class AProductUnverified(api_resource.ApiResource):
	"""
	未审核的商品信息
	"""
	app = "product"
	resource = "product_unverified"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		corp = args['corp']
		product_id = args.get('product_id')

		product_unverified_data = corp.global_product_repository.get_product_unverified(product_id)

		base_info = product_unverified_data['base_info']
		models_info = product_unverified_data['models_info']
		image_info = product_unverified_data['image_info']
		logistics_info = product_unverified_data['logistics_info']

		return {
			'owner_id': product_unverified_data['owner_id'],
			'name': base_info['name'],
			'promotion_title': base_info['promotion_title'],
			'price_info': {
				'display_price':base_info['price']
			},
			'postage_id': logistics_info['postage_id'],
			'has_same_postage': logistics_info['postage_type'] == 'unified_postage_type',
			'has_multi_models': bool(models_info['custom_models']),
			'weight': models_info['standard_model']['weight'],
			'stocks': models_info['standard_model']['stocks'],
			'detail': base_info['detail'],
			'models': {
				'standard_model': models_info['standard_model'],
				'custom_models': models_info['custom_models']
			},
			'images': image_info['images'],
			'limit_zone_type': logistics_info['limit_zone_type'],
			'limit_zone': logistics_info['limit_zone_id'],
			'postage_money': logistics_info['unified_postage_money'],
			'classification_id': base_info['classification_id'],
			'classification_name_nav': ProductClassificationRepository.get(corp).get_product_classification(base_info['classification_id']).get_nav()
		}

	@param_required(['corp_id', 'product_id', 'base_info:json', 'models_info:json', 'image_info:json', 'logistics_info:json'])
	def put(args):
		corp = args['corp']
		product_id = args.get('product_id')

		product = corp.global_product_repository.get_product(product_id)

		product.update_product_unverified(args)

		return {}
