# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator

from util import upyun_util




class Image(business_model.Model):
	"""
	图片分组
	"""
	__slots__ = (
		'id',
		'owner_id',
		'group_id',
		'title',
		'url',
		'width',
		'height',
		'created_at',
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	def empty_image(model=None):
		return Image(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		return Image(model)

	@staticmethod
	@param_required(['owner_id', 'image_id'])
	def from_id(args):
		image = mall_models.Image.select().dj_where(owner_id=args['owner_id'], id=args['image_id'])
		return Image(image)


	@property
	def group(self):
		return self.context['db_model'].group
	
	def save(self, params):
		mall_models.Image.create(**params)