# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_label_group import ProductLabelGroup


class AProductLableGroup(api_resource.ApiResource):
	"""
	商品标签分类
	"""
	app = 'mall'
	resource = 'product_label_group'

	@param_required(['corp_id','name'])
	def put(args):
		"""
		创建标签分类
		:return:
		"""
		result = ProductLabelGroup.create({
			'corp_id': args['corp_id'],
			'name': args['name']
		})
		if isinstance(result, basestring):
			return (500, result)
		else:
			return {'id': result.id}

	@param_required(['id'])
	def delete(args):
		"""
		删除标签分类
		:return:
		"""
		ProductLabelGroup.delete({'id': args['id']})
		return {}

