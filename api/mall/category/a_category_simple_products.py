# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category.category_product_repository import CategoryProductRepository
from business.mall.corporation_factory import CorporationFactory


class ACategorySimpleProducts(api_resource.ApiResource):
	app = 'mall'
	resource = 'category_simple_products'

	@param_required(['category_ids'])
	def get(args):
		corp = CorporationFactory.get_weizoom_corporation()
		category_ids = json.loads(args['category_ids'])
		results = []
		for category_id in category_ids:
			products = CategoryProductRepository.get(corp).get_simple_products_for_category(category_id)
			results.append({
				'category_id': category_id,
				'product_ids': [p.id for p in products]
			})
		
		return results
