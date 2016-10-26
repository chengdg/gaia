# -*- coding: utf-8 -*-

from eaglet.core import api_resource

class AProductLableGroups(api_resource.ApiResource):
	"""
	商品标签集合
	"""
	app = 'mall'
	resource = 'product_label_groups'

	def get(args):
		corp = args['corp']
		product_label_groups = corp.product_label_group_repository.get_label_groups()

		datas = []
		for group in product_label_groups:
			group_has_labels = group.get_labels()
			labels = [{"label_id": label.id, "label_name": label.name} for label in group_has_labels]
			datas.append({
				'label_group_id': group.id,
				'label_group_name': group.name,
				'labels': labels
			})

		return {
			'product_label_groups': datas
		}