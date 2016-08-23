# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog

from business.mall.category import Category
from business.mall.category_has_product import CategoryHasProduct
from business.mall.category_factory import CategoryFactory
from business.mall.category_has_product_factory import CategoryHasProductFactory
from business.mall.product import Product

class ACategory(api_resource.ApiResource):
	app = 'mall'
	resource = 'category'

	@param_required(['name', 'owner_id'])
	def post(args):
		# print 'post++++++++++====category.....', args
		'''
		创建商品分组,  利用工厂类@生成器
		'''
		category_factory_obj = CategoryFactory.create()
		category_obj = category_factory_obj.save(args['owner_id'], args['name'])
		return  {
			'category':category_obj.to_dict() 
		}

	@param_required(['category_id', 'name'])
	def put(args):
		category_obj = Category.fromId({'category_id': args['category_id']})
		if category_obj:
			try:
				category_obj.updateName(args['category_id'], args['name'])
				return {}
			except Exception, e:
				 watchdog.error(message=e)
				 return e.message
		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return msg

	@param_required(['category_id'])
	def get(args):
		category_id = args['category_id']
		category_obj = Category.fromId({'category_id': category_id})
		if category_obj:
			ret = {
				'category': category_obj.to_dict()
			}
			if args.get('is_has_product', None):
				ret['category'].update({
					'products': [product.to_dict() for product in category_obj.products]
				})
			return ret
		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return msg


	@param_required(['category_id'])
	def delete(args):
		category_obj = Category.fromId({'category_id': args['category_id']})
		if  category_obj.products:  # 分组内有商品
			CategoryHasProduct.emptyCateogryHasProduct().deleteFromModel(category_obj)
		if category_obj:
			action_count = category_obj.deleteFromId(args['category_id'])
			return {}

