# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator

from business.mall.image import Image


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
	@param_required(['owner_id'])
	def from_owner(args):
		image_groups = mall_models.ImageGroup.select().dj_where(owner=args['owner_id'])
		if image_groups:
			return [ImageGroup(image_group) for image_group in image_groups]
		else:
			return []

	@staticmethod
	@param_required(['owner_id', 'image_group_id'])
	def from_id(args):
		image_group = mall_models.ImageGroup.select().dj_where(owner=args['owner_id'], id=args['image_group_id'])
		if image_group.first():
			return ImageGroup(image_group.first())
		else:
			return None

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

	@property
	def images(self):
		images = mall_models.Image.select().dj_where(group=self.context['db_model'])
		if images:

			self.context['images'] = [Image.from_model({'db_model': image}) for image in images]
			return self.context['images']
		else:
			return []

	@images.setter
	def images(self, value):
		self.context['images'] = value


	def delete(self, owner_id, image_group_id):
		mall_models.ImageGroup.delete().dj_where(owner=owner_id, id=image_group_id).execute()

	def update(self, owner_id, image_group_id,params):
		mall_models.ImageGroup.update(**params).dj_where(owner=owner_id, id=image_group_id).execute()




