# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image_group.image_group import ImageGroup

class AImageGroup(api_resource.ApiResource):
	'''
	图片分组
	'''
	app = 'mall'
	resource = 'image_group'

	@param_required(['corp_id', 'image_group_id'])
	def get(args):
		corp = args['corp']
		image_group = corp.image_group_repository.get_image_group(args['image_group_id'])
		
		if image_group:
			data = {
				"id": image_group.id,
				"name": image_group.name,
				"images": [],
				"created_at": image_group.created_at.strftime('%Y-%m-%d %H:%M')
			}

			for image in image_group.images:
				data['images'].append({
					"id": image.id,
					"url": image.url,
					"width": image.width,
					"height": image.height
				})

			return {
				'image_group': data
			}
		else:
			return 500, "image group not found"

	@param_required(['corp_id', 'name', 'images'])
	def put(args):
		images = json.loads(args['images'])
		image_group = ImageGroup.create(args['corp'], args['name'], images)

		return {
			'id': image_group.id
		}

	@param_required(['corp_id', 'image_group_id'])
	def post(args):
		corp = args['corp']
		image_group = corp.image_group_repository.get_image_group(args['image_group_id'])

		if image_group:
			name = args['name']
			images = json.loads(args['images'])
			image_group.update({
				"name": name, 
				"images": images
			})

			return {}
		else:
			msg = u'image_group_id {} not exist'.format(args['image_group_id'])
			return 500, {'msg': msg}

	@param_required(['corp_id', 'image_group_id'])
	def delete(args):
		corp = args['corp']
		corp.image_group_repository.delete_image_group(args['image_group_id'])

		return {}