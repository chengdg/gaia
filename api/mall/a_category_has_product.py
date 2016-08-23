# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog

from business.mall.category import Category
from business.mall.category_has_product import CategoryHasProduct
from business.mall.product import Product
from business.mall.category_has_product_factory import CategoryHasProductFactory

class ACategoryHasProducts(api_resource.ApiResource):
	app = 'mall'
	resource = 'category_has_product'

	@param_required(['category_id', 'product_ids'])
	def post(args):
		#由于在zeus测试平台，不能传列表，现由'1,2,3,4,5'这种方式处理
		product_ids = [product_id.strip() for product_id in args.get('product_ids', '').strip().split(',') if product_id]
		args.update({"product_ids": product_ids})
		# if not product_ids:
		#     msg = u'商品列表不能为空'
		#     watchdog.error(message=msg)
		#     return msg           
		category_obj = Category.fromId({'category_id': args['category_id']})
		if category_obj:
			flag = False
			for product_id in args['product_ids']:
				product_obj = Product.from_id({'product_id': product_id})
				if not product_obj:
					msg = u'{}商品不存在'.format(product_id)
					flag = True
					watchdog.error(message=msg)
					break
			if flag:
				return msg
			else:
				# TODO 创建分组商品   @工厂生成器
				try:
					category_has_product_obj = CategoryHasProductFactory.create()
					category_has_products = category_has_product_obj.save(product_ids, category_obj)
					product_count = len(category_has_products)
					# TODO 更新分组的内容--产品个数
					product_count += int(category_obj.product_count)
					category_obj.updateProductCount(args['category_id'], product_count)
				except Exception, e:
					watchdog.error(message=str(e))
				return {}

		else:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return 500, msg

	@param_required(['category_id', 'product_id'])
	def get(args):
		if args.get('category_has_product_id', None):
			category_has_product_obj = CategoryHasProduct.fromId({'category_has_product_id': args['category_has_product_id']})
			if category_has_product_obj:
				category_has_product_dict = category_has_product_obj.to_dict()
				category_has_product_dict.update({
					'category': category_has_product_obj.category.to_dict(),
					'product': category_has_product_obj.product.to_dict()
				})
				return category_has_product_dict
			else:
				msg = u'{}不存在'.format(args['category_has_product_id'])
				watchdog.error(message=msg)
				return 500, msg
		else:
			category_obj = Category.fromId({'category_id': args['category_id']})
			if not category_obj:
				msg = u'{}不存在'.format(args['category_id'])
				watchdog.error(message=msg)
				return msg 
			product_obj = Product.from_id({'product_id': args['product_id']})     
			if not product_obj:
				msg = u'{}不存在'.format(args['product_id'])
				watchdog.error(message=msg)
				return 500, msg 

			category_has_product_obj= CategoryHasProduct.fromCategoryIdAndProduct_id({'category_id': args['category_id'], 'product_id': args['product_id']})
			if category_has_product_obj:
				return {
					'category_has_product': category_has_product_obj.to_dict()
				}
			else:
				msg = u'分组{0},商品{1}没有关联关系'.format(args['category_id'], args['product_id'])
				watchdog.error(message=msg)
				return 500, msg

	@param_required(['category_id', 'product_id'])
	def delete(args):
		category_obj = Category.fromId({'category_id': args['category_id']})
		if not category_obj:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return 500, msg 
		product_obj = Product.from_id({'product_id': args['product_id']})     
		if not product_obj:
			msg = u'{}不存在'.format(args['product_id'])
			watchdog.error(message=msg)
			return 500, msg 
		category_has_product_obj= CategoryHasProduct.fromCategoryIdAndProduct_id({'category_id': args['category_id'], 'product_id': args['product_id']})
		if category_has_product_obj:
			action_count = category_has_product_obj.deleteFromId(category_has_product_obj.to_dict()['id'])
			return {}
	@param_required(['category_id', 'product_id', 'position'])
	def put(args):
		category_obj = Category.fromId({'category_id': args['category_id']})
		if not category_obj:
			msg = u'{}不存在'.format(args['category_id'])
			watchdog.error(message=msg)
			return 500, msg 
		product_obj = Product.from_id({'product_id': args['product_id']})     
		if not product_obj:
			msg = u'{}不存在'.format(args['product_id'])
			watchdog.error(message=msg)
			return 500, msg 
		category_has_product_obj= CategoryHasProduct.fromCategoryIdAndProduct_id({'category_id': args['category_id'], 'product_id': args['product_id']})
		if category_has_product_obj: 
			category_has_product_obj.updatePosition(args['category_id'], args['product_id'], args['position'])
			return {}