# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image_group.image_group import ImageGroup

class AImageGroups(api_resource.ApiResource):
	'''
	图片分组
	'''
	app = 'mall'
	resource = 'image_groups'

	@param_required(['corp_id'])
	def get(args):
		'''
		图片分组列表
		'''
		corp = args['corp']
		image_groups = corp.image_group_repository.get_image_groups()

		datas = []
		for image_group in image_groups:
			data = {
				"id": image_group.id,
				"name": image_group.name,
				"images": [],
				"created_at": image_group.created_at.strftime('%Y-%m-%d %H:%M')
			}

			for image in image_group.images[:6]: #在group列表中，一个group最多显示6张图片
				data['images'].append({
					"id": image.id,
					"url": image.url,
					"width": image.width,
					"height": image.height
				})
			datas.append(data)

		return {
			'image_groups': datas
		}
