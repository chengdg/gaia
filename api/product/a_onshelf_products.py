# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product
from business.product.product_shelf import ProductShelf
from business.common.page_info import PageInfo


class AProductOnshelf(api_resource.ApiResource):
	"""
	待售商品管理

	"""
	app = "product"
	resource = "onshelf_products"

	@param_required(['corp'])
	def get(args):
		'''
		待售商品列表
		'''
		corp = args['corp']
		in_sale_shelf = corp.insale_shelf
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		products, pageinfo = in_sale_shelf.get_products(target_page)

		opt = {
			'owner_id': args['owner_id'],
			'shelve_type': 1,   #int 0 在售标志 
			'is_deleted': False,
			'fill_options': {
				'with_selected_category': True,
				'with_all_category': True,
				'with_image': True,
				'with_property': True,
				'with_group_buy_info': True,
				'with_sales': True,
				'with_product_promotion': True,
				'with_price': True,
				'with_product_model': True
			} # 填充参数
		}

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': []
		}

	@param_required(['ids'])
	def put(args):
		"""
		上架商品
		@return:
		"""

		return "success"