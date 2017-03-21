# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory
from business.common.page_info import PageInfo


class AProductCategories(api_resource.ApiResource):
	app = 'mall'
	resource = 'product_categories'

	@param_required(['product_id'])
	def get(args):
		corp = CorporationFactory.get_weizoom_corporation()
		product_id = args['product_id']
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		categories, page_info = corp.category_repository.get_product_categories(product_id, target_page)
		
		data = []
		for category in categories:
			data.append({
				'id': category.id,
				"owner_id": category.owner_id,
				'name': category.name
			})
		return {
			"categories": data,
			'page_info': page_info.to_dict()
		}

