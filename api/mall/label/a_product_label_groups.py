# -*- coding: utf-8 -*-

from eaglet.core import api_resource

from business.mall.corporation_factory import CorporationFactory


class AProductLableGroups(api_resource.ApiResource):
	"""
	商品标签集合
	"""
	app = 'mall'
	resource = 'product_label_groups'

	def get(args):
		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		product_label_groups = weizoom_corp.product_label_group_repository.get_label_groups()

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