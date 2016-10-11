# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category.category import Category

class ACategoryProducts(api_resource.ApiResource):
	app = 'mall'
	resource = 'category_products'

	@param_required(['corp_id', 'category_id', 'product_ids'])
	def put(args):
		corp = args['corp']
		product_ids = json.loads(args['product_ids'])
		category_ids = json.loads(args['category_id'])
		if type(category_ids) == int:
			#category_ids是一个id
			category_ids = [category_ids]

		for category_id in category_ids:
			category = corp.category_repository.get_category(category_id)
			category.add_products(product_ids)

		return {}

