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

	@param_required(['classification_id:int'])
	def get(args):
		"""
		:return:

		[{
			'label_group_id': label_group_A,
			'label_ids': [label_a1, label_a2, label_a3]
		},{
			'label_group_id': label_group_B,
			'label_ids': [label_b1, label_b2, label_b3]
		}]
		"""
		classification_id = args['classification_id']
		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
		classification_label_models = classification.get_classification_labels()

		label_group_has_label = {}
		for model in classification_label_models:
			label_group_id = model.label_group_id
			label_id = model.label_id
			if not label_group_has_label.has_key(label_group_id):
				label_group_has_label[label_group_id] = [label_id]
			else:
				label_group_has_label[label_group_id].append(label_id)

		return_data = []
		for label_group_id, label_ids in label_group_has_label.items():
			return_data.append({
				'label_group_id': label_group_id,
				'label_ids': label_ids
			})

		return return_data



	@param_required(['classification_id', 'selected_labels:json'])
	def put(args):
		"""
		设置商品分类标签
		"""
		classification_id = args['classification_id']
		selected_labels = args['selected_labels']

		print selected_labels

		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
		classification.set_labels(selected_labels)

		return {}

