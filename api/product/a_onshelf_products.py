# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo

from a_offshelf_products import AOffshelfProducts

class AOnshelfProducts(api_resource.ApiResource):
	"""
	在售商品集合
	"""
	app = "product"
	resource = "onshelf_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		products, pageinfo = corp.insale_shelf.get_products(target_page)

		datas = []
		for product in products:
			data = {
				"id": product.id,
				"name": product.name,
				"create_type": product.create_type,
				"image": product.thumbnails_url,
				"models_info": AOffshelfProducts._get_models_info(product),
				"user_code": -1,
				"bar_code": product.bar_code,
				"categories": AOffshelfProducts._get_categories(product),
				"price": None,
				"sales": product.sales,
				"created_at": product.created_at.strftime('%Y-%m-%d %H:%M'),
				"sync_at": product.sync_at.strftime('%Y-%m-%d %H:%M') if product.create_type == 'sync' else None,
				"is_use_custom_model": product.is_use_custom_model,
				"display_index": product.display_index,
				'supplier': AOffshelfProducts._get_supplier(product),
				'classifications': AOffshelfProducts._get_classifications(product)
			}

			if product.is_use_custom_model:
				data['stock_type'] = 'combined'
				data['stocks'] = -1
				data['price'] = 'todo'
			else:
				standard_model = product.standard_model
				data['stock_type'] = standard_model.stock_type
				data['stocks'] = standard_model.stocks
				data['price'] = standard_model.price

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