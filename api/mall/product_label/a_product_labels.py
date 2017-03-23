# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory


class AProductLable(api_resource.ApiResource):
	"""
	商品标签
	"""
	app = 'mall'
	resource = 'product_labels'

	@param_required(['corp_id'])
	def get(args):
		corp = CorporationFactory.get()
		labels = corp.product_label_repository.get_labels()
		return [{
			'id': label.id,
			'name': label.name,
			'label_group_id': label.label_group_id,
			'created_at': label.created_at.strftime('%Y-%m-%d %H:%M:%S')
		} for label in labels]