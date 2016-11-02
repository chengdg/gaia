# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.cps.product_promote import ProductPromote
from business.cps.product_promote_repository import ProductPromoteRepository
from business.common.page_info import PageInfo
from business.product.encode_product_service import EncodeProductService


class AProductPoolPromote(api_resource.ApiResource):
	"""

	"""
	app = 'cps'
	resource = 'product_pool_promotes'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})
		filters = json.loads(args.get('filters', '{}'))
		product_promote_repository = corp.product_promote_repository
		promotes, page_info = product_promote_repository.get_product_pool_promotes(target_page, filters)
		result = []
		encode_product_service = EncodeProductService.get(corp)
		for promote in promotes:
			product = promote.product
			base_info = encode_product_service.get_base_info(product)
			models_info = encode_product_service.get_models_info(product)
			supplier = encode_product_service.get_supplier_info(product)
			classifications = encode_product_service.get_classifications(product)
			image_info = encode_product_service.get_image_info(product)
			categories = encode_product_service.get_categories(product)
			temp_dict = {
				'id': promote.id,
				'promote_money': promote.promote_money,
				'promote_stock': promote.promote_stock,
				'promote_time_from': promote.promote_time_from,
				'promote_time_to': promote.promote_time_to,
				'promote_sale_count': promote.promote_sale_count,
				'promote_total_money': promote.promote_total_money,
				'product':  {
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
					"display_index": base_info['display_index'],
					'supplier': supplier,
					'classifications': classifications
				}
			}
			result.append(temp_dict)
		return {
			'pageinfo': page_info.to_dict(),
			'product_promotes': result
		}
