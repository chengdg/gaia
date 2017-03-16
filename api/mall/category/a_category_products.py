# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo

from business.mall.category.category_product_repository import CategoryProductRepository
from business.product.encode_product_service import EncodeProductService


class ACategoryProducts(api_resource.ApiResource):
	app = 'mall'
	resource = 'category_products'

	@param_required(['corp_id', 'category_id', 'product_ids'])
	def put(args):
		corp = args['corp']
		product_ids = json.loads(args['product_ids'])
		category_ids = json.loads(args['category_id'])
		if type(category_ids) == int:
			#category_ids是一个id
			category_ids = [category_ids]

		for category_id in category_ids:
			category = corp.category_repository.get_category(category_id)
			category.add_products(product_ids)

		return {}
	
	@param_required(['corp_id', 'category_id'])
	def get(args):
		corp = args['corp']
		category_id = args['category_id']
		fill_options = json.loads(args.get('fill_options', '{}'))
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		category = corp.category_repository.get_category(category_id)
		products, page_info = CategoryProductRepository.get(category)\
			.get_on_shelf_products_for_category(category_id, corp.id, fill_options=fill_options, target_page=target_page)
		
		encode_product_service = EncodeProductService.get(corp)
		
		data = []
		for product in products:
			temp_value = dict()
			temp_value['id'] = product.id
			
			if 'with_base' in fill_options:
				base_info = encode_product_service.get_base_info(product)
				temp_value['base_info'] = base_info
			data.append(temp_value)
			# 其他一次类推
		return {
			"products": data,
			'page_info': page_info.to_dict()
		}
		# category = corp.category_repository.get_products(page_info, fill_options=fill_options)
