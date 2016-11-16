# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.product.encode_product_service import EncodeProductService
from db.mall import models as mall_models


class AUnshelfConsignmentProducts(api_resource.ApiResource):
	"""
	未在货架上的代销商品
	"""
	app = "product"
	resource = "unshelf_consignment_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		filters = json.loads(args.get('filters', '{}'))
		filters['__f-status-equal'] = mall_models.PP_STATUS_ON_POOL

		fill_options = {
			'with_category': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_shelve_status': True,
			'with_supplier_info': True,
			'with_classification': True,
			'with_sales': True,
			'with_product_label': True,
			'with_cps_promotion_info': True,
		}

		options = {
			'order_options': ['display_index', '-id']
		}

		products, pageinfo = corp.product_pool.get_products(target_page, fill_options, options, filters)

		encode_product_service = EncodeProductService.get(corp)
		datas = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			models_info = encode_product_service.get_models_info(product)
			supplier = encode_product_service.get_supplier_info(product)
			classifications = encode_product_service.get_classifications(product)
			image_info = encode_product_service.get_image_info(product)
			categories = encode_product_service.get_categories(product)
			labels = encode_product_service.get_labels(product)
			cps_promotion_info = encode_product_service.get_cps_promotion_info(product)

			data = {
				"id": product.id,
				"name": base_info['name'],
				"create_type": base_info['create_type'],
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
				'labels': labels,
				"cps_promotion_info": cps_promotion_info,

			}

			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': datas
		}

	@param_required(['corp_id', 'product_ids'])
	def put(args):
		corp = args['corp']
		product_ids = json.loads(args['product_ids'])
		corp.forsale_shelf.delete_products(product_ids)

		return {}
