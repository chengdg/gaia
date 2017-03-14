# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AProductLabel(api_resource.ApiResource):
	"""
	商品标签
	"""
	app = "product"
	resource = "product_label"

	@param_required(['corp_id', 'product_id:int', 'classification_id:int'])
	def get(args):
		corp = args['corp']
		product_id = args['product_id']
		classification_id = args['classification_id']
		product = corp.global_product_repository.get_product(product_id)
		labels = product.get_labels(classification_id)

		return [{
			'label_id': l.id,
			'label_name': l.name,
			'label_group_id': l.label_group_id
		} for l in labels]

	@param_required(['corp_id', 'product_id:int', 'label_ids:json'])
	def put(args):
		corp = args['corp']
		product_id = args['product_id']
		label_ids = args['label_ids']

		product = corp.global_product_repository.get_product(product_id)
		product.manage_label(label_ids)

		return {}

		