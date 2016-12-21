# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory


class AProductClassificationLabel(api_resource.ApiResource):
	"""
	商品分类标签
	"""
	app = "mall"
	resource = "product_classification_label"

	@param_required(['corp_id', 'classification_id:int'])
	def get(args):
		"""
		:return:
		:classification_has_own_label: 商品分类是否有自己的标签而不是继承自上级分类
		"""
		classification_id = args['classification_id']
		corp = CorporationFactory.get()
		classification = corp.product_classification_repository.get_product_classification(classification_id)
		relation_data = classification.get_label_group_relation()

		return {
			'relations': relation_data['relations'],
			'classification_has_own_label': relation_data['classification_has_own_label']
		}

	@param_required(['corp_id', 'classification_id', 'selected_labels:json'])
	def put(args):
		"""
		设置商品分类标签
		"""
		classification_id = args['classification_id']
		selected_labels = args.get('selected_labels', [])

		corp = CorporationFactory.get()
		classification = corp.product_classification_repository.get_product_classification(classification_id)
		classification.set_labels(selected_labels)

		return {}

