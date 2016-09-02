# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator


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

	def __init__(self, model=None):
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
		image = mall_models.Image.select().dj_where(owner=args['owner_id'], id=args['image_id'])
		if image.first():
			return Image(image.first())
		else:
			return None

	@property
	def group(self):
		return self.context['db_model'].group.to_dict()
	
	def save(self, params):
		image = mall_models.Image.create(**params)
		return Image(image)

	def delete_from_group(self, image_group):
		mall_models.Image.delete().dj_where(group=image_group.context['db_model']).execute()

	def delete(self):
		self.context['db_model'].delete_instance()
		# mall_models.Image.delete().dj_where(owner=owner_id, id=image_id).execute()

	def create(self, params):
		opt = {
			'owner': params['owner_id'],
			'group': params['group_id'],
			'url': params['image_path'],
			'width': params['width'],
			'height': params['height'],
			'title': params['title']
		}
		return self.save(opt)


