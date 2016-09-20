# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.image import Image


class AImage(api_resource.ApiResource):
	'''
	图片
	'''
	app = 'mall'
	resource = 'image'

	@param_required(['owner_id', 'image_id'])
	def get(args):
		'''
		图片
		'''
		params = args
		opt = {
			'owner_id': params['owner_id'],
			'image_id': params['image_id']
		}
		image = Image.from_id(opt)
		return {
			'image': image
		}

	@param_required(['owner_id', 'group_id', 'image_path', 'width', 'height'])
	def put(args):
		'''
		添加图片 利用工厂类@生成器
		'''
		print args
		opt = {
			'owner_id': args['owner_id'],
			'group_id': args['group_id'],
			'image_path': args['image_path'],
			'width': args['width'],
			'height': args['height'],
			'title': args.get('title', '')
		}
		image = Image().create(opt)
		return {
			'image':image
		}
	@param_required(['owner_id'])
	def post(args):
		pass

	@param_required(['owner_id', 'image_id'])
	def delete(args):
		image = Image.from_id({'owner_id': args['owner_id'], 'image_id': args['image_id']})
		if image:
			image.delete()
			return {}
		else:
			msg = u'image_id {} 不存在'.format(args['image_id'])
			return 500, {'msg': msg}

