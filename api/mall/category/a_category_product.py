# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category.category import Category

class ACategoryProduct(api_resource.ApiResource):
	app = 'mall'
	resource = 'category_product'

	@param_required(['corp_id', 'category_id', 'product_id', 'field', 'value'])
	def post(args):
		corp = args['corp']
		field = args['field']
		value = args['value']
		product_id = args['product_id']
		category = corp.category_repository.get_category(args['category_id'])
		if field == 'position':
			category.update_product_position(product_id, value)
		else:
			pass

		return {}

	@param_required(['corp_id', 'category_id', 'product_id'])
	def delete(args):
		corp = args['corp']
		category = corp.category_repository.get_category(args['category_id'])
		category.delete_product(args['product_id'], corp)

		return {}

