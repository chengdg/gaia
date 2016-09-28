# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.category import Category
from business.common.page_info import PageInfo

class ACategoryCandidateProducts(api_resource.ApiResource):
	'''
	可以加入ctegory的product集合
	'''
	app = 'mall'
	resource = 'category_candidate_products'

	@param_required(['corp', 'category_id'])
	def get(args):
		category_id = args['category_id']
		corp = args['corp']
		if category_id == '0':
			#没有指定category，获取全部商品
			count_per_page = args.get('count_per_page', 10)
			query = {}
			target_page = PageInfo(args.get('page', 1), count_per_page)
			products, pageinfo = corp.product_pool.get_products(query, target_page)
		else:
			products = []

		datas = []
		for product in products:
			data = {
				"id": product.id,
				"name": product.name,
				"sales": product.sales,
				"status": product.shelve_type,
				"updated_at": product.created_at.strftime('%Y-%m-%d %H:%M'),
				"price": 0
			}
			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': datas
		}
