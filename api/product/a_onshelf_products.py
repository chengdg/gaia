# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo

from business.product.encode_product_service import EncodeProductService

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

		filters = json.loads(args.get('filters', '{}'))
		if filters:
			products, pageinfo = corp.insale_shelf.search_products(filters, target_page)
		else:
			products, pageinfo = corp.insale_shelf.get_products(target_page)

		encode_product_service = EncodeProductService.get(corp)
		datas = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			models_info = encode_product_service.get_models_info(product)
			supplier = encode_product_service.get_supplier_info(product)
			classifications = encode_product_service.get_classifications(product)
			image_info = encode_product_service.get_image_info(product)
			categories = encode_product_service.get_categories(product)

			data = {
				"id": product.id,
				"name": base_info['name'],
				"create_type": base_info['create_type'],
				"is_member_product": base_info['is_member_product'],
				"image": image_info['thumbnails_url'],
				"models_info": models_info,
				"bar_code": base_info['bar_code'],
				"display_index": base_info['display_index'],
				'supplier': supplier,
				'classifications': classifications,
				"categories": categories,
				"sales": base_info['sales'],
				"created_at": base_info['created_at'],
				"sync_at": base_info['sync_at'],
				"display_index": base_info['display_index'],
				'supplier': supplier,
				'classifications': classifications
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