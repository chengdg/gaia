# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product import Product


class AProductOffshelf(api_resource.ApiResource):
	"""
	待售商品管理

	"""
	app = "product"
	resource = "product_offshelf"

	@param_required(['owner_id'])
	def get(args):
		'''
		待售商品列表
		'''
		opt = {
			'owner_id': args['owner_id'],
			'shelve_type': 0,   #int 0 待售标志 
			'is_deleted': False,
			'fill_options': {} # 填充参数
		}
		products = Product.from_owner_id(opt)
		return {
			'products': products
		}