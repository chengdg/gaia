# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_pending_stock.pending_stock_product import PendingProduct

class APendingProduct(api_resource.ApiResource):
	"""
	待入库商品
	"""
	app = "mall"
	resource = "pending_stock_product"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		corp = args['corp']
		product_id = args.get('product_id')
		product_model = PendingProduct.get(product_id)
		
		classification_id = product_model.classification_id
		classifications = corp.product_classification_repository.get_product_classification_tree_by_end(classification_id)
		classification_name_nav = '--'.join([classification.name for classification in classifications])

		return {
			'id': product_model.id,
			'product_name': product_model.name,
			'title': product_model.title,
			'price': str(product_model.product_price) if product_model.product_price > 0 else str(product_model.settlement_price),
			'settlement_price': str(product_model.settlement_price),
			'weight': '%s' % product_model.weight,
			'store': product_model.store,
			'has_limit_time': product_model.has_limit_time,
			'valid_time_from': '' if not product_model.valid_time_from else product_model.valid_time_from.strftime(
				"%Y-%m-%d %H:%M"),
			'valid_time_to': '' if not product_model.valid_time_to else product_model.valid_time_to.strftime("%Y-%m-%d %H:%M"),
			'limit_settlement_price': str(product_model.limit_settlement_price),
			'remark': product_model.remark,
			'product_model': [], #TODO
			'images': [],
			'limit_zone_type': product_model.limit_zone_type,
			'limit_zone_id': product_model.limit_zone,
			'has_same_postage': product_model.has_same_postage,
			'postage_money': '%.2f' % product_model.postage_money,
			'classification_name_nav': classification_name_nav
		}

	@param_required(['corp_id', 'name'])
	def put(args):
		pending_product, msg = PendingProduct.create({
			'owner_id': args['corp'].id,
			'name': args['name'],
			'title': args.get('title', ''),
			'has_product_model': args.get('has_product_model', False),
			'price': args.get('price', 0),
			'weight': args.get('weight', 0),
			'store': args.get('store', 0),
			'limit_zone_type': args.get('limit_zone_type', 0),
			'limit_zone': args.get('limit_zone', 0),
			'postage_id': args.get('postage_id', 0),
			'postage_money': args.get('postage_money', 0),
			'has_same_postage': args.get('has_same_postage', True),
			'remark': args.get('remark', '')
		})

		if pending_product:
			return {}
		else:
			return (500, msg)





		