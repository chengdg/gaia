# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.image_group.image import Image
from business.mall.corporation_factory import CorporationFactory


class ImageGroup(business_model.Model):
	"""
	图片分组
	"""
	__slots__ = (
		'id',
		'name',
		'created_at',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		return ImageGroup(args['db_model'])

	@property
	def images(self):
		"""
		获取image group中的Image对象集合
		"""
		image_models = mall_models.Image.select().dj_where(group_id=self.id)
		images = []
		for image_model in image_models:
			images.append(Image.from_model(image_model))

		return images

	def add_image(self, corp, image):
		"""
		向image group中添加一个image
		"""
		mall_models.Image.create(
			owner = corp.id,
			group = self.id,
			url = image['path'],
			title = '',
			width = image['width'],
			height = image['height']
		)

	def update(self, params):
		"""
		更新image group
		"""
		corp = CorporationFactory.get()
		mall_models.Image.delete().dj_where(owner_id=corp.id, group_id=self.id).execute()

		if 'name' in params:
			#更新name
			mall_models.ImageGroup.update(name=params['name']).dj_where(owner_id=corp.id, id=self.id).execute()

		if 'images' in params:
			#更新images
			for image in params['images']:
				self.add_image(corp, image)

	@staticmethod
	def create(corp, name, images):
		image_group_model = mall_models.ImageGroup.create(
			owner = corp.id,
			name = name
		)

		image_group = ImageGroup.from_model({
			'db_model': image_group_model
		})

		for image in images:
			image_group.add_image(corp, image)

		return image_group



