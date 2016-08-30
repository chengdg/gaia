# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image_group_factory import ImageGroupFactory
from business.mall.image_group import ImageGroup
from business.mall.image import Image
from business.mall.image_factory import ImageFactory

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
		images = []
		if 'images' in params:
			# TODO 如果在添加分组时添加图片
			images = []
		image_group_factory = ImageGroupFactory.create()
		image_group = image_group_factory.save(args['owner_id'], args['name'], images=images)

		return {
			'image_group': image_group
		}

	@param_required(['owner_id', 'image_group_id'])
	def put(args):
		params = {}
		images = []
		if 'name'in args:
			params['name'] = args['name']
		if 'images' in args:
			# images = [
			# 	{
			# 		'owner': 3,
			# 		'group': 3,
			# 		'image_path': '/home/rocky/Pictures/001.png',
			# 		'width': 200,
			# 		'height': 300
			# 	}
			# ]
			images = json.loads(args['images'])
		image_group = ImageGroup.from_id({'owner_id': args['owner_id'], 'image_group_id': args['image_group_id']})
		if image_group:
			if images:
				image = Image.empty_image()
				image.update(args['owner_id'], image_group)
				for image in images:
					image_factory = ImageFactory.create()
					image_factory.save(image)
			image_group.update(args['owner_id'], args['image_group_id'], params)
			return {}
		else:
			msg = u'image_group_id %s 不存在'.formate(args['image_group_id'])
			return 500, {'msg': msg}

	@param_required(['owner_id', 'image_group_id'])
	def delete(args):
		image_group = ImageGroup.from_id({'owner_id': args['owner_id'], 'image_group_id': args['image_group_id']})
		if image_group:
			if image_group.images:
				image = Image.empty_image()
				image.delete_group(image_group)
			image_group.delete(args['owner_id'], args['image_group_id'])
			return {}
		else:
			msg = u'image_group_id %s 不存在'.formate(args['image_group_id'])
			return 500, {'msg': msg}

	@param_required(['owner_id', 'image_group_id'])
	def get(args):
		image_group = ImageGroup.from_id({'owner_id': args['owner_id'], 'image_group_id': args['image_group_id']})
		if image_group:
			return {
				'image_group': image_group.to_dict('images')
			}

		else:
			msg = u'image_group_id {} 不存在'.format(args['image_group_id'])
			return 500, {'msg': msg}