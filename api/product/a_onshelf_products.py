# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo


class AOnshelfProducts(api_resource.ApiResource):
	"""
	在售商品集合
	"""
	app = "product"
	resource = "onshelf_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		in_sale_shelf = corp.insale_shelf
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		products, pageinfo = in_sale_shelf.get_products(target_page)

		datas = []
		for product in products:
			data = {
				"id": product.id,
				"name": product.name,
				"image": product.thumbnails_url,
				"models": product.models,
				"user_code": -1,
				"bar_code": product.bar_code,
				"categories": [],
				"price": None,
				"stocks": -1,
				"sales": product.sales,
				"created_at": product.created_at.strftime('%Y-%m-%d %H:%M'),
				"is_use_custom_model": product.is_use_custom_model,
				"display_index": product.display_index
			}
			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': datas
		}

	@param_required(['corp', 'product_ids'])
	def put(args):
		corp = args['corp']
		product_ids = json.loads(args['product_ids'])
		corp.insale_shelf.move_products(product_ids)

		return {}