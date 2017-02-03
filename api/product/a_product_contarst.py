# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.global_product_repository import GlobalProductRepository
from business.product.product import Product


class AProductContrast(api_resource.ApiResource):
	"""
	最后一次审核通过的商品信息
	"""
	app = "product"
	resource = "product_contrast"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		product_id = args.get('product_id')


		product_contrast = GlobalProductRepository.get().get_product_contrast(product_id)

		
		return {
			# 'product_id': pre_product_contrast.product_id,
			# 'name': pre_product.name,
			# 'promotion_title': pre_product.promotion_title,
			# 'price_info': pre_product.price_info,
			# 'weight': '0.00' if not pre_product.standard_model else '%.2f' % pre_product.standard_model.weight,
			# 'stocks': pre_product.stocks,
			# 'detail': pre_product.detail,
			# 'models': pre_product.custom_models,
			# 'images': pre_product.swipe_images,
			# 'limit_zone_type': pre_product.limit_zone_type,
			# 'limit_zone': pre_product.limit_zone,
			# 'has_same_postage': pre_product.has_same_postage,
			# 'has_multi_models': pre_product.has_multi_models,
			# 'postage_money': '%.2f' % pre_product.unified_postage_money,
			# 'classification_id': pre_product.classification_id,
			# 'classification_name_nav': pre_product.classification_nav,
		}

	@param_required(['corp_id', 'product_id:int'])
	def put(args):
		product_id = args.get('product_id')

		product = GlobalProductRepository.get().get_product(product_id)

		product.update_product_contrast(args['corp'])

		return {}

		