# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo

class APendingProducts(api_resource.ApiResource):
	"""
	待入库商品集合
	"""
	app = "mall"
	resource = "pending_stock_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		page_info = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		pageinfo, preview_products = corp.pending_product_repository.filter_products(args, page_info)

		rows = []

		for product in preview_products:
			classification_name_nav = '--'.join([classification.name for classification in corp.product_classification_repository.get_product_classification_tree_by_end(product.classification_id)])
			rows.append({
				'id': product.id,
				'owner_id': corp.id,
				'classificationId': product.classification_id,
				'product_name': product.product_name,
				'customer_name': '', #?
				'total_sales': 0, #TODO 获取已入库商品的销量
				'product_status': product.get_stock_status_text(),
				'product_status_value': 0, #?
				'classification_name_nav': classification_name_nav,
				'is_update': product.is_update,
				'customer_from_text': '', #?
				'refuse_reason': product.refuse_reason,
				'labelNames': [] #TODO商品标签
			})

		return {
			'rows': rows,
			'pageinfo': pageinfo.to_dict()
		}
		