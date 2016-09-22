# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category import Category

class ACategoryProducts(api_resource.ApiResource):
	'''
	'''
	app = 'mall'
	resource = 'category_products'

	@param_required(['owner_id', 'category_ids'])
	def get(args):
		'''
		获得促销活动可以选用的分组商品集合.
		# '''

		category_ids = [category_id.strip() for category_id in args['category_ids'].strip().split(',') if category_id]
		category_products = []
		for category_id in category_ids:
			category = Category.from_id({'category_id': category_id})
			category_products += category.products
		return {
			'category_products': [category_product.to_dict() for category_product in category_products]
		}

