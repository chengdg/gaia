# -*- coding: utf-8 -*-
import json
import copy

from eaglet.core import api_resource
from eaglet.decorator import param_required


from business.mall.category import Category
from business.common.page_info import PageInfo

class ACategories(api_resource.ApiResource):
	"""
	商品分组集合
	"""
	app = 'mall'
	resource = 'categories'

	@param_required(['corp'])
	def get(args):
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})
		
		categories, pageinfo = args['corp'].category_repository.get_all_categories(target_page)

		datas = []
		for category in categories:
			datas.append({
				"id": category.id,
				"name": category.name,
				
				"products": [],
				"created_at": category.created_at.strftime('%Y-%m-%d %H:%M')
			})

		return {
			'pageinfo': pageinfo.to_dict(),
			'categories': datas
		}