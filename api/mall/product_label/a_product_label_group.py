# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_label.product_label_group import ProductLabelGroup
from business.mall.corporation_factory import CorporationFactory


class AProductLableGroup(api_resource.ApiResource):
	"""
	商品标签分类
	"""
	app = 'mall'
	resource = 'product_label_group'

	@param_required(['corp_id', 'label_group_name'])
	def put(args):
		"""
		创建标签分类
		:return:
		"""
		result = ProductLabelGroup.create(args['label_group_name'])
		if isinstance(result, basestring):
			return (500, result)
		else:
			return {'id': result.id}

	@param_required(['corp_id', 'label_group_id'])
	def delete(args):
		"""
		删除标签分类
		:return:
		"""
		corp = CorporationFactory.get()
		corp.product_label_group_repository.delete_label_group(args['label_group_id'])

		return {}

