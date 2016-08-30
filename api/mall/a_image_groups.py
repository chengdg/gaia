# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image_group import ImageGroup

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
		image_groups = ImageGroup.from_owner({'owner_id': params['owner_id']})
		if 'is_display_images' in args:
			image_groups = [image_group.to_dict('images') for image_group in image_groups]
		else:
			image_groups = [image_group.to_dict() for image_group in image_groups]
		return {
			'image_groups': image_groups
		}

