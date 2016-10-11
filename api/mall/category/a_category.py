# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category.category import Category
from business.common.page_info import PageInfo

class ACategory(api_resource.ApiResource):
	app = 'mall'
	resource = 'category'

	@param_required(['corp_id', 'category_id'])
	def get(args):
		corp = args['corp']

		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		category = corp.category_repository.get_category(args['category_id'])
		category_products, pageinfo = category.get_products(target_page)

		data = {
			"id": category.id,
			"name": category.name,
			"pageinfo": pageinfo.to_dict(),
			"products": [],
			"created_at": category.created_at.strftime('%Y-%m-%d %H:%M')
		}
		for category_product in category_products:
			data['products'].append({
				"id": category_product.id,
				"name": category_product.name,
				"price": category_product.price,
				"display_index": category_product.display_index,
				"status": category_product.status,
				"sales": category_product.sales,
				"categories": category_product.categories,
				"created_at": category_product.created_at.strftime('%Y-%m-%d %H:%M')
			})

		return data

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

