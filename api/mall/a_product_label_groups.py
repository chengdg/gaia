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
		product_label_groups = corp.product_label_repository.get_label_groups()

		datas = []
		for group in product_label_groups:
			datas.append({
				'label_group_id': group.id,
				'label_group_name': group.name,
				'labels': group.labels
			})

		return {
			'product_label_groups': datas
		}