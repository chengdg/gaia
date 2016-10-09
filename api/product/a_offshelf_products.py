# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo


class AOffshelfProducts(api_resource.ApiResource):
	"""
	待售商品集合
	"""
	app = "product"
	resource = "offshelf_products"

	@staticmethod
	def _get_models_info(product):
		"""
		获得商品的models_info数据
		"""
		models_info = {
			'is_use_custom_model': False,
			'standard_model': None,
			'custom_models': None,
			'used_system_model_properties': None
		}
		models_info['is_use_custom_model'] = product.is_use_custom_model

		standard_model = product.standard_model
		if standard_model:
			models_info['standard_model'] = {
				"name": standard_model.name,
				"price": standard_model.price,
				"weight": standard_model.weight,
				"stock_type": standard_model.stock_type,
				"stocks": standard_model.stocks,
				"user_code": standard_model.user_code
			}
		else:
			models_info['standard_model'] = None
		
		custom_models = product.custom_models
		if custom_models:
			for custom_model in custom_models:
				models_info['custom_models'].append({
					"name": custom_model.name,
					"price": custom_model.price,
					"weight": custom_model.weight,
					"stock_type": custom_model.stock_type,
					"stocks": custom_model.stocks,
					"user_code": custom_model.user_code
				})
		else:
			models_info['custom_models'] = []

		return models_info

	@staticmethod
	def _get_categories(product):
		"""
		获得商品的category集合
		"""
		categories = []
		for category in product.categories:
			categories.append({
				"id": category['id'],
				"name": category['name']
			})

		return categories

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		products, pageinfo = corp.forsale_shelf.get_products(target_page)

		datas = []
		for product in products:
			data = {
				"id": product.id,
				"name": product.name,
				"image": product.thumbnails_url,
				"models": [],
				"user_code": -1,
				"bar_code": product.bar_code,
				"categories": AOffshelfProducts._get_categories(product),
				"price": None,
				"sales": product.sales,
				"created_at": product.created_at.strftime('%Y-%m-%d %H:%M'),
				"is_use_custom_model": product.is_use_custom_model,
				"display_index": product.display_index
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

	@param_required(['corp'])
	def put(args):
		corp = args['corp']
		product_ids = json.loads(args['product_ids'])
		corp.forsale_shelf.move_products(product_ids)

		return {}