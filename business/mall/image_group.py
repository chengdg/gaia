# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator




class ImageGroup(business_model.Model):
	"""
	图片分组
	"""
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'created_at',
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	def empty_image_group(model=None):
		return ImageGroup(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		image_group = ImageGroup(model)
		return image_group

	def save(self, owner_id, name, images=None):
		opt = {
			'owner': owner_id,
			'name': name
		}
		image_group, created = mall_models.ImageGroup.get_or_create(**opt)
		return ImageGroup(image_group)