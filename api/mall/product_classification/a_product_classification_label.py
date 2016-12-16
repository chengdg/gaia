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

		all_label_ids = []
		label_id2classifi = dict()
		for model in classification_label_models:
			label_id = model.label_id
			all_label_ids.append(label_id)
			label_id2classifi[label_id] = model.classification_id

		label_models = weizoom_corp.product_label_repository.get_labels(all_label_ids)

		label_group_has_label = dict()
		label_relation = dict()
		for model in label_models:
			label_group_id = model.label_group_id
			label_id = str(model.id)
			if not label_group_has_label.has_key(label_group_id):
				label_group_has_label[label_group_id] = [label_id]
			else:
				label_group_has_label[label_group_id].append(label_id)

			label_relation[label_id] = True if int(label_id2classifi[label_id]) == int(classification_id) else False

		return_data = []
		for label_group_id, label_ids in label_group_has_label.items():
			return_data.append({
				'labelGroupId': label_group_id,
				'labelIds': list(set(label_ids)) #去重
			})
		return {
			'selected_labels': return_data,
			'label_relation': label_relation
		}

	@param_required(['classification_id', 'selected_labels:json'])
	def put(args):
		"""
		设置商品分类标签
		"""
		classification_id = args['classification_id']
		selected_labels = args['selected_labels']

		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
		classification.set_labels(selected_labels)

		return {}

