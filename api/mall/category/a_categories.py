# -*- coding: utf-8 -*-
import json
import copy

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo

class ACategories(api_resource.ApiResource):
	"""
	商品分组集合
	"""
	app = 'mall'
	resource = 'categories'

	@param_required(['corp_id'])
	def get(args):
		should_return_product = (args.get('return_product', 'false') == 'true')
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})
		
		corp = args['corp']

		filters = json.loads(args.get('filters', '[]'))
		if filters:
			categories, pageinfo = corp.category_repository.search_categories(filters)
		else:
			categories, pageinfo = corp.category_repository.get_all_categories(target_page)

		datas = []
		for category in categories:
			data = {
				"id": category.id,
				"name": category.name,
				
				"products": [],
				"created_at": category.created_at.strftime('%Y-%m-%d %H:%M')
			}

			if should_return_product:
				for category_product in category.top_ten_products:
					data['products'].append({
						"id": category_product.id,
						"name": category_product.name,
						"price": category_product.price,
						"display_index": category_product.display_index,
						"status": category_product.status,
						"sales": category_product.sales,
						"created_at": category_product.created_at.strftime('%Y-%m-%d %H:%M')
					})

			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict() if pageinfo else None,
			'categories': datas
		}