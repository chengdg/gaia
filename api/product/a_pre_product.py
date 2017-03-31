# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService


class APreProduct(api_resource.ApiResource):
	"""
	原始商品
	"""
	app = "product"
	resource = "pre_product"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		corp = args['corp']
		product_id = args.get('product_id')

		fill_options = {
			'with_price': True,
			'with_image': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_classification': True,
			'with_product_label': True
		}

		pre_product = corp.global_product_repository.get_product(product_id, fill_options)
		
		return {
			'id': pre_product.id,
			'owner_id': pre_product.owner_id,
			'name': pre_product.name,
			'owner_name': corp.details.company_name,
			'company_name': corp.details.company_name,
			'axe_sales_name': corp.details.axe_sales_name,
			'promotion_title': pre_product.promotion_title,
			'price_info': pre_product.price_info,
			'weight': '0.00' if not pre_product.standard_model else '%.2f' % pre_product.standard_model.weight,
			'stocks': pre_product.stocks,
			'detail': pre_product.detail,
			'models': {
				'standard_model': pre_product.standard_model,
				'custom_models': pre_product.custom_models
			},
			'images': pre_product.swipe_images,
			'limit_zone_type': pre_product.limit_zone_type,
			'limit_zone': pre_product.limit_zone,
			'has_same_postage': pre_product.has_same_postage,
			'has_multi_models': pre_product.has_multi_models,
			'postage_id': pre_product.postage_id,
			'postage_money': '%.2f' % pre_product.unified_postage_money,
			'classification_id': pre_product.classification_id,
			'label_ids': [label.id for label in pre_product.labels],
			'classification_name_nav': pre_product.classification_nav,
			'status': pre_product.status,
			'is_accepted': pre_product.is_accepted,
			'refuse_reasons': pre_product.refuse_reasons,
			'is_updated': pre_product.is_updated
		}

	@param_required(['corp_id', 'base_info:json', 'models_info:json', 'image_info:json', 'logistics_info:json'])
	def put(args):

		product_factory = ProductFactory.get(args['corp'])
		result = product_factory.create_product({
			'corp': args['corp'],
			'base_info': args['base_info'],
			'models_info': args['models_info'],
			'logistics_info': args['logistics_info'],
			'image_info': args['image_info']
		})

		if result:
			return {}
		else:
			return 500, u'商品名已存在'

	@param_required(['corp_id', 'product_id', 'base_info:json', 'models_info:json', 'image_info:json', 'logistics_info:json'])
	def post(args):
		product_id = args['product_id']

		update_product_service = UpdateProductService.get(args['corp'])
		update_product_service.update_product(product_id, {
			'corp': args['corp'],
			'base_info': args['base_info'],
			'models_info': args['models_info'],
			'logistics_info': args['logistics_info'],
			'image_info': args['image_info']
		})

		return {}

	@param_required(['corp_id', 'product_id:int'])
	def delete(args):
		product_id = args['product_id']
		corp = args['corp']
		corp.product_pool.delete_products([product_id])

		return {}


		