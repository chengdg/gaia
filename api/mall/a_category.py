# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category import Category
from business.mall.category_factory import CategoryFactory
from business.mall.product import Product

class ACategory(api_resource.ApiResource):
	app = 'mall'
	resource = 'category'

	@param_required(['name', 'owner_id'])
	def post(args):
		'''
		创建商品分组,  利用工厂类@生成器
		'''
		category_factory = CategoryFactory.create()
		category = category_factory.save(args['owner_id'], args['name'], product_ids=args.get('product_ids', None))
		return  {
			'category':category
		}

	@param_required(['owner_id','category_id'])
	def put(args):
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

	@param_required(['owner_id', 'category_id'])
	def delete(args):
		category = Category.from_id({'category_id': args['category_id']})
		if category:
			if 'product_id' not in args:
				category.delete_from_id(args['category_id'])
			else:
				category.delete_product(args['category_id'], args['product_id'])
			return {}
		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return 500, {'message': msg}

