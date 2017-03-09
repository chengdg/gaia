# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource

from business.mall.corporation_factory import CorporationFactory


class ASimpleEffectiveProducts(api_resource.ApiResource):
	"""
	所有有效商品简单数据
	"""
	app = 'product'
	resource = 'simple_effective_products'

	def get(args):
		"""
		
		"""
		corp = CorporationFactory.get_weizoom_corporation()
		products = corp.product_pool.get_simple_effective_products()
		data = []
		for product in products:
			data.append({
				"id": product.id,
				"name": product.name,
			})

		return {
			"products": data
		}
