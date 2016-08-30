# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.image_group import ImageGroup

class ImageGroupFactory(business_model.Model):
	'''
	分组创建工厂@生成器
	'''
	__slots__=()
	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	def create():
		image_group_factory = ImageGroupFactory()
		return image_group_factory

	def save(self, owner_id, name, images=None):
		image_group = ImageGroup.empty_image_group()

		return image_group.save(owner_id, name, images)
