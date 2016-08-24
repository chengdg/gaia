# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog

from business.mall.category import Category
from business.mall.category_product import CategoryProduct
from business.mall.category_factory import CategoryFactory
from business.mall.category_product_factory import CategoryProductFactory
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
		category = category_factory.save(args['owner_id'], args['name'])
		return  {
			'category':category.to_dict() 
		}

	@param_required(['owner_id','category_id', 'name'])
	def put(args):
		category = Category.from_id({'category_id': args['category_id']})
		if category:
			try:
				category.update_name(args['category_id'], args['name'])
				return {}
			except:
			            msg = unicode_full_stack()
			            watchdog.error(msg)
		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return msg

	@param_required(['owner_id', 'category_id'])
	def delete(args):
		category = Category.from_id({'category_id': args['category_id']})
		if  category.products:  # 分组内有商品
			CategoryProduct.empty_cateogry_product().delete_from_model(category)
		if category_obj:
			action_count = category_obj.delete_from_id(args['category_id'])
			return {}
		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return 500, msg

