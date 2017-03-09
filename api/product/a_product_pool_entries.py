# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.product.encode_product_service import EncodeProductService


class AProductPoolEntries(api_resource.ApiResource):
	"""
	在售卖的商品(简单数据目前缓存在用)
	"""
	app = "product"
	resource = "product_pool_entries"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		product_pools = corp.insale_shelf.get_product_pool_entries()
		data = []
		for pool in product_pools:
			
			temp_data = {
				"id": pool.product_id,
				"display_index": pool.display_index,
				"sync_at": pool.sync_at,
			}
			data.append(temp_data)

		return {
			'products': data
		}
