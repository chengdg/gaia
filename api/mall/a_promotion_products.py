# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product import Product

class APromotionProducts(api_resource.ApiResource):
	'''
	获得促销活动可以选用的商品集合.
	'''
	app = 'mall'
	resource = 'promotion_products'

	@param_required(['owner_id', 'type'])
	def get(args):
		'''
		获得促销活动可以选用的商品集合.
		@param type "usable_promotion_products" or "promotion_products"
		'''
		promotion_product_type = args.get('type', 'promotion_products')
		if promotion_product_type == 'usable_promotion_products':
			promotion_products, page_info = Product.promotion_products({
				'owner_id': args['owner_id'],
				'cur_page': args.get('cur_page', 1),
				'count_per_page': args.get('count_per_page', 10),
				'fill_options': {
								"with_product_model": True,
								"with_model_property_info": True,
								'with_sales': True,
								'with_product_promotion': True,
								'with_is_select': True
								}
			})
			return {
				'pageinfo': page_info.to_dict(),
				'promotion_products': [promotion_product.to_dict() for promotion_product in promotion_products]
			}
		elif promotion_product_type == 'promotion_products':
			promotion_products = Product.promotion_products({
				'owner_id': args['owner_id'],
				'promotion_id': args['promotion_id'],   # 在type=promotion_products 时
				'fill_options': {"with_product": True}
			})
			return {
				'promotion_products': [promotion_product.to_dict() for promotion_product in promotion_products]
			}
		else:
			return {}
