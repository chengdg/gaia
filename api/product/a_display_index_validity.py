# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.mall.corporation_factory import CorporationFactory
from business.product.encode_product_service import EncodeProductService

class ADisplayIndexValidity(api_resource.ApiResource):
	"""
	商品排序的有效性信息
	"""
	app = "product"
	resource = "display_index_validity"

	@param_required(['corp_id', 'display_index'])
	def get(args):
		corp = args['corp']
		display_index = args['display_index']
		if corp.product_pool.has_product_with_display_index(display_index):
			return {
				'is_exists': True
			}
		else:
			return {
				'is_exists': False
			}
