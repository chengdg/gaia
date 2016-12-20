# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class APendingProduct(api_resource.ApiResource):
	"""
	待入库商品
	"""
	app = "mall"
	resource = "pending_product"

	@param_required(['corp_id', '?product_id:int', '?classification_id:int'])
	def get(args):
		corp = args['corp']
		product_id = args.get('product_id')
		product_has_model = 0
		if product_id:
			product_model = corp.pending_product_repository.get_pending_product(product_id)
			classification_id = product_model.classification_id
			stock_status = product_model.get_stock_status_text()
		else:
			classification_id = args.get('classification_id', 0)
			stock_status = u'待入库'

		models = corp.product_classification_repository.get_product_classification_tree_by_end(classification_id)
		classification_name_nav = '--'.join([model.name for model in models])

		limit_zone_info = []

		return {
			'product_has_model': product_has_model,
			'stock_status': stock_status,
			'limit_zone_info': limit_zone_info,
			'classification_name_nav': classification_name_nav
		}






		