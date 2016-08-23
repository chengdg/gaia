# -*- coding: utf-8 -*-
import json
import pdb

from eaglet.core import api_resource
from eaglet.decorator import param_required

from core import paginator
from business.mall.category import Category

class ACategories(api_resource.ApiResource):
	"""
	商品管理
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
		if 'category_ids' not in args:
			args['category_ids'] = 'all'
		category_ids = [category_id.strip() for category_id in args['category_ids'].strip().split(',') if category_id]
		# print '00077&&&&&&&&&&&&&&&.................',args, category_ids
		if 'all' in category_ids and len(category_ids) == 1:
			category_ids = list()
		elif 'all' in category_ids and len(category_ids) > 1:
			category_ids.remove('all')
		args.update({'category_ids': category_ids})
		category_objs = Category.getForCategory(args)

		# 分页
		page_info = {
			'page': int(args['page']) if 'page' in args else 1,
			'count_per_page': int(args['count_per_page']) if 'count_per_page' in args else 10
		}
		# 是否在分组中显示商品信息
		if args.get('is_display_products', None):
			page_info.update({'is_display_products': args['is_display_products']})
		return  ACategories.getPageinfoPaginator(category_objs, is_paginator=not args['category_ids'], **page_info)

	@staticmethod
	def getPageinfoPaginator(category_models, is_paginator=False, **kwargs):
		"""
		分页管理
		"""
		print category_models, is_paginator, kwargs
		is_display_products = kwargs.get('is_display_products', None)
		if is_paginator:
			cur_page = kwargs.get('page')
			count_per_page = kwargs.get('count_per_page')
			query_string = kwargs.get('query_string', None)
			pageinfo, categories = paginator.paginate(category_models, cur_page, count_per_page, query_string=query_string) 
			ret = {
				'categories': [category.to_dict() for category in categories],
				'pageinfo': pageinfo.to_dict()
			}
			if is_display_products:
				display_products = ACategories.categoryDisplayProducts(categories)
				ret.update({'categories': display_products})
			return ret
		else:
			ret = {
				'categories': [category_model.to_dict() for category_model in category_models]
			}
			if is_display_products:
				display_products = ACategories.categoryDisplayProducts(category_models)
				ret.update({'categories': display_products})
			return ret

	@staticmethod
	def categoryDisplayProducts(categpory_list):
		category_has_product_list = []
		# import pdb
		# pdb.set_trace()
		for category in categpory_list:
			category_obj = category.to_dict()
			category_obj.update({
				'products': [product.to_dict() for product in category.products]
			}) 
			category_has_product_list.append(category_obj)
		return category_has_product_list
