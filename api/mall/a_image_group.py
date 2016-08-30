# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image_group_factory import ImageGroupFactory

class AImageGroup(api_resource.ApiResource):
	'''
	图片分组
	'''
	app = 'mall'
	resource = 'image_group'

	@param_required(['owner_id', 'name'])
	def post(args):
		'''
		创建图片分组 利用工厂类@生成器
		'''
		params = args
		images = None
		if 'images' in params:
			# TODO 如果在添加分组时添加图片
			images = []
		image_group_factory = ImageGroupFactory.create()
		return image_group_factory.save(args['owner_id'], args['name'], images=images)

