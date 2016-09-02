# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image_group import ImageGroup
from business.mall.image import Image

class AImageGroup(api_resource.ApiResource):
	'''
	图片分组
	'''
	app = 'mall'
	resource = 'image_group'

	@param_required(['owner_id', 'name'])
	def put(args):
		'''
		创建图片分组 利用工厂类@生成器
		'''
		images = []
		if 'images' in args:
			# TODO 如果在添加分组时添加图片
			# 格式
			# images = [
			# 	{
			# 		'image_path': '/home/rocky/Pictures/001.png',
			# 		'width': 200,
			# 		'height': 300,
			# 		'title': args.get('title', '')
			# 	}
			# ]
			images = json.loads(args['images'])
		image_group = ImageGroup().create(args['owner_id'], args['name'], images=images)
		# image_group = image_group_factory.save()

		return {
			'image_group': image_group.to_dict()
		}

	@param_required(['owner_id', 'image_group_id'])
	def post(args):
		'''
		更新图片
		'''
		params = {}
		images = []
		if 'name'in args:
			params['name'] = args['name']
		if 'images' in args:
			# images = [
			# 	{
			# 		'image_path': '/home/rocky/Pictures/001.png',
			# 		'width': 200,
			# 		'height': 400,
			# 		'title': args.get('title', '')
			# 	}
			# ]
			images = json.loads(args['images'])
		image_group = ImageGroup.from_id({'owner_id': args['owner_id'], 'image_group_id': args['image_group_id']})
		if image_group:
			image_group.update(params=params, images=images)
			return {}
		else:
			msg = u'image_group_id {} not exist'.format(args['image_group_id'])
			return 500, {'msg': msg}

	@param_required(['owner_id', 'image_group_id'])
	def delete(args):
		image_group = ImageGroup.from_id({'owner_id': args['owner_id'], 'image_group_id': args['image_group_id']})
		if image_group:
			image_group.delete()
			return {}
		else:
			msg = u'image_group_id {} not exist'.format(args['image_group_id'])
			return 500, {'msg': msg}

	@param_required(['owner_id', 'image_group_id'])
	def get(args):
		image_group = ImageGroup.from_id({'owner_id': args['owner_id'], 'image_group_id': args['image_group_id']})
		if image_group:
			return {
				'image_group': image_group.to_dict('images')
			}

		else:
			msg = u'image_group_id {} not exist'.format(args['image_group_id'])
			return 500, {'msg': msg}