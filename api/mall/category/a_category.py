# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category.category import Category

class ACategory(api_resource.ApiResource):
	app = 'mall'
	resource = 'category'

	@param_required(['corp_id', 'name'])
	def put(args):
		'''
		'''
		name = args['name']
		corp = args['corp']
		if 'product_ids' in args:
			product_ids = json.loads(args['product_ids'])
		else:
			product_ids = None
		category = Category.create(corp, name, product_ids)

		return  {
			'category': {
				"id": category.id,
				"name": category.name
			}
		}

	@param_required(['corp_id', 'category_id', 'field', 'value'])
	def post(args):
		corp = args['corp']
		field = args['field']
		value = args['value']
		category = corp.category_repository.get_category(args['category_id'])
		if field == 'name':
			category.update_name(value)
		else:
			pass

		return {}

	@param_required(['corp_id', 'category_id'])
	def delete(args):
		corp = args['corp']
		corp.category_repository.delete_category(args['category_id'])
		
		return {}

