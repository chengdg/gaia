# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory


class AProductLableGroups(api_resource.ApiResource):
	"""
	商品标签集合
	"""
	app = 'mall'
	resource = 'product_label_groups'

	@param_required(['corp_id'])
	def get(args):
		corp = CorporationFactory.get()
		product_label_groups = corp.product_label_group_repository.get_label_groups()

		product_labels = corp.product_label_repository.get_labels_by_group_ids([p.id for p in product_label_groups])
		product_label_group_id2labels = dict()

		for label in product_labels:
			if not product_label_group_id2labels.has_key(label.label_group_id):
				product_label_group_id2labels[label.label_group_id] = [label]
			else:
				product_label_group_id2labels[label.label_group_id].append(label)

		datas = []
		for group in product_label_groups:
			group_has_labels = product_label_group_id2labels.get(group.id, [])
			labels = [{"label_id": label.id, "label_name": label.name} for label in group_has_labels]
			datas.append({
				'label_group_id': group.id,
				'label_group_name': group.name,
				'labels': labels
			})
		return {
			'product_label_groups': datas
		}