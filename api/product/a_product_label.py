# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory
from business.product.global_product_repository import GlobalProductRepository


class AProductLabel(api_resource.ApiResource):
	"""
	商品标签
	"""
	app = "product"
	resource = "product_label"

	@param_required(['corp_id', 'product_id:int', 'classification_id:int'])
	def get(args):
		#首先获取商品分类包含的标签
		classification_id = args['classification_id']
		corp = CorporationFactory.get()
		classification = corp.product_classification_repository.get_product_classification(classification_id)
		relation_data = classification.get_label_group_relation()

		#再获取商品直属的标签
		product_has_labels = corp.product_label_repository.get_labels_oweto_product_id(args['product_id'])

		return {
			'relations': relation_data['relations'],
			'classification_has_own_label': relation_data['classification_has_own_label'],
			'product_has_labels': [{
				'label_id': p.id,
				'label_name': p.name
			} for p in product_has_labels]
		}

	@param_required(['corp_id', 'product_id:int', 'label_ids:json'])
	def put(args):
		product_id = args['product_id']
		label_ids = args['label_ids']

		pre_product = GlobalProductRepository.get().get_product(product_id)
		pre_product.manage_label(label_ids)

		return {}

		