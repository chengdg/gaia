# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.common.page_info import PageInfo
from business.mall.category.category_product_repository import CategoryProductRepository

class ACategoryCandidateProducts(api_resource.ApiResource):
	'''
	可以加入ctegory的product集合
	'''
	app = 'mall'
	resource = 'category_candidate_products'

	@param_required(['corp_id', 'category_id'])
	def get(args):
		category_id = int(args['category_id'])
		corp = args['corp']

		#分页信息
		cur_page = int(args.get('page', 1))
		count_per_page = int(args.get('count_per_page', 10))
		target_page = PageInfo(cur_page, count_per_page)

		category_products, pageinfo = CategoryProductRepository.get(corp).get_candidate_products_for_category(category_id, target_page)

		datas = []
		for category_product in category_products:
			data = {
				"id": category_product.id,
				"name": category_product.name,
				"sales": category_product.sales,
				"status": category_product.status,
				"updated_at": category_product.created_at.strftime('%Y-%m-%d %H:%M'),
				"price": category_product.price
			}
			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': datas
		}
