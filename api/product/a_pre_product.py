# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.global_product_repository import GlobalProductRepository
from business.product.product_factory import ProductFactory

class APreProduct(api_resource.ApiResource):
	"""
	原始商品
	"""
	app = "product"
	resource = "pre_product"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		product_id = args.get('product_id')

		fill_options = {
			'with_category': False,
			'with_price': True,
			'with_image': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_property': False,
			'with_supplier_info': True,
			'with_classification': True,
			'with_product_promotion': False
		}

		pre_product = GlobalProductRepository.get().get_product(product_id, fill_options)
		
		return {
			'id': pre_product.id,
			'name': pre_product.name,
			'promotion_title': pre_product.promotion_title,
			'price_info': pre_product.price_info,
			'weight': pre_product.weight,
			'stocks': pre_product.stocks,
			'detail': pre_product.detail,
			'models': [pre_product.standard_model] if pre_product.standard_model else pre_product.custom_models,
			'images': pre_product.swipe_images,
			'limit_zone_type': pre_product.limit_zone_type,
			'limit_zone': pre_product.limit_zone,
			'has_same_postage': pre_product.has_same_postage,
			'postage_money': '%.2f' % pre_product.unified_postage_money,
			'classification_name_nav': pre_product.classification_nav
		}

	@param_required(['corp_id', 'name', '?has_multi_models:bool', '?models:json'])
	def put(args):
		name = args['name']
		promotion_title = args.get('promotion_title', '')
		price = args['price']
		weight = args['weight']
		stocks = args['stocks']
		purchase_price = args.get('purchase_price', 0.0)
		detail = args.get('detail', '')
		postage_id = args.get('postage_id', 0)
		postage_type = 'unified_postage_type' if args['has_same_postage'] else 'custom_postage_type'
		limit_zone_type = args.get('limit_zone_type', 0)
		limit_zone = args.get('limit_zone', 0)
		unified_postage_money = args['postage_money']
		has_multi_models = args['has_multi_models']
		models = args.get('models', [])
		classification_id = args['classification_id']

		base_info = {
			'name': name,
			'promotion_title': promotion_title,
			'detail': detail,
			'price': price,
			'purchase_price': purchase_price,
			'classification_id': classification_id,
			'is_pre_product': True
		}

		image_info = args.get('images', {'images': []})

		postage_info = {
			'postage_type': postage_type,
			'postage_id': postage_id,
			'unified_postage_money': unified_postage_money,
			'limit_zone_type': limit_zone_type,
			'limit_zone': limit_zone
		}

		models_info = {
			'is_use_custom_model': has_multi_models,
			'standard_model': {
				'price': price,
				'purchase_price': purchase_price,
				'weight': weight,
				'stocks': stocks,
				'stock_type': 'limit',
			},
			'custom_models': models
		}
		product_factory = ProductFactory.get(args['corp'])
		product_factory.create_product({
			'corp': args['corp'],
			'base_info': base_info,
			'models_info': models_info,
			'logistics_info': postage_info,
			'image_info': image_info
		})

		return {}

	def post(self):
		pass

	def delete(self):
		pass





		