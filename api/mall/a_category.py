# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category import Category

class ACategory(api_resource.ApiResource):
	app = 'mall'
	resource = 'category'

	@param_required(['corp', 'name'])
	def put(args):
		'''
		创建商品分组,  利用工厂类@生成器
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

	@param_required(['owner_id','category_id'])
	def post(args):
		# 修改分组
		category = Category.from_id({'category_id': args['category_id']})
		params = {}
		if category:
			try:
				if 'name' in args:
					params['name'] = args['name']
					category.update_category_property(args['category_id'], update_params=params)
				if 'display_index' in args and 'product_id' in args:
					params['display_index'] = args['display_index']
					params['product_id'] = args['product_id']
					category.update_category_property(args['category_id'],actionProperty='position', update_params=params)
				if 'product_ids' in args:
					params['product_ids'] = args['product_ids']
					category.update_category_property(args['category_id'],actionProperty='products', update_params=params)
				return {}
			except:
				msg = unicode_full_stack()
				watchdog.error(msg)
				return 500, {}
		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return 500, {'message': msg}

	@param_required(['corp', 'category_id'])
	def delete(args):
		corp = args['corp']
		corp.category_repository.delete_category(args['category_id'])
		
		return {}

