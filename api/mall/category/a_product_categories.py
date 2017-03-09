# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category.category import Category
from business.mall.corporation_factory import CorporationFactory


class AProductCategories(api_resource.ApiResource):
	app = 'mall'
	resource = 'product_categories'

	@param_required(['product_id'])
	def get(args):
		corp = CorporationFactory.get_weizoom_corporation()
		product_id = args['product_id']
		
		categories = corp.category_repository.get_product_categories(product_id)
		results = [dict(id=category.id,
						owner_id=category.owner_id) for category in categories]
		return {
			"categories": results
		}

