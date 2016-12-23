# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory


class AProductLable(api_resource.ApiResource):
	"""
	商品标签
	"""
	app = 'mall'
	resource = 'product_label'

	@param_required(['corp_id', 'label_group_id:int', 'label_name'])
	def put(args):
		"""
		创建标签
		"""
		corp = CorporationFactory.get()
		label_group = corp.product_label_group_repository.get_label_group(args['label_group_id'])
		result = label_group.add_label(args['label_name'])

		if isinstance(result, basestring):
			return (500, result)
		else:
			return {
				'label': {
					'id': result.id,
					'name': result.name,
					'label_group_id': result.label_group_id,
					'created_at': result.created_at.strftime('%Y-%m-%d %H:%M:%S')
				}
			}

	@param_required(['corp_id', 'label_id:int'])
	def delete(args):
		"""
		删除标签
		"""
		corp = CorporationFactory.get()
		corp.product_label_repository.delete_labels([args['label_id']])

		return {}

