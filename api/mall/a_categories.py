# -*- coding: utf-8 -*-
import json
import copy

from eaglet.core import api_resource
from eaglet.decorator import param_required

from core import paginator
from business.mall.category import Category

class ACategories(api_resource.ApiResource):
	"""
	商品分组管理
	"""
	app = 'mall'
	resource = 'categories'

	@param_required(['owner_id'])
	def get(args):
		"""
		商品管理---> 分组管理列表
		@param category_ids:分组id列表
		"""
		# 由于在zeus测试平台，不能传列表，现由'1,2,3,4,5'这种方式处理
		params = {'owner_id': args['owner_id']}

		if 'category_ids' not in args:
			category_ids = list()
		else:
			category_ids = [category_id.strip() for category_id in args['category_ids'].strip().split(',') if category_id]
		params.update({'category_ids': category_ids})
		# 分页
		page_info = {
			'cur_page': int(args.get('page', 1)),
			'count_per_page': int(args.get('count_per_page', 10))
		}
		params.update(page_info)

		if 'is_display_products' in args:
			params['is_display_products'] = True
		categories, pageinfo = Category.get_categories(params)
		return {
			'pageinfo': pageinfo,
			'categories': [category.to_dict('products') for category in categories] if params.get('is_display_products', None) else categories
		}