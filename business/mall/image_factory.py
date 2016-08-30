# -*- coding: utf-8 -*-
import logging
import time

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.image import Image

class ImageFactory(business_model.Model):
	'''
	图片 创建工厂@生成器
	'''
	__slots__=()
	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	def create():
		image_factory = ImageFactory()
		return image_factory

	def save(self, params):
		image = Image.empty_image()
		opt = {
			'owner': params['owner_id'],
			'group': params['group_id'],
			'url': params['image_path'],
			'width': params['width'],
			'height': params['height'],
			'title': params['title']
		}
		return image.save(opt)
