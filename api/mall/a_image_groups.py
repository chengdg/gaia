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
	resource = 'image_groups'

	@param_required(['owner_id'])
	def get(args):
		'''
		图片分组列表
		'''
		params = args
		return []

