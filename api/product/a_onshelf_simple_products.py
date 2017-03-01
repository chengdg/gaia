# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.product.encode_product_service import EncodeProductService


class AOnshelfSimpleProducts(api_resource.ApiResource):
	"""
	在售卖的商品(简单数据目前缓存在用)
	"""
	app = "product"
	resource = "onshelf_simple_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		filters = json.loads(args.get('filters', '{}'))
		products, pageinfo = corp.insale_shelf.get_simple_products(target_page, filters)

		encode_product_service = EncodeProductService.get(corp)
		datas = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			price_info = encode_product_service.get_price_info(product)
			categories = encode_product_service.get_categories(product)

			data = {
				"id": product.id,
				"name": base_info['name'],
				"create_type": base_info['create_type'],
				"is_member_product": base_info['is_member_product'],
				"bar_code": base_info['bar_code'],
				"display_index": base_info['display_index'],
				"created_at": base_info['created_at'],
				"sync_at": base_info['sync_at'],
				"price_info": price_info,
				"categories": categories,
				"thumbnails_url": base_info['thumbnails_url'],
			}

			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': datas
		}
