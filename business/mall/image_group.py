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

	def __init__(self, model=None):
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

	def __save(self, owner_id, name, images=None):
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


	def delete(self):
		if self.images:
			Image().delete_from_group(self)
		self.context['db_model'].delete_instance()

	def update(self, params=None, images=None):
		'''
		更新分组内容
		'''
		# import pdb
		# pdb.set_trace()
		if params:
			# 主要是name
			self.context['db_model'].name = params['name']
			self.context['db_model'].save()
		if images:
			mall_models.Image.delete().dj_where(group=self.context['db_model']).execute()
			for image in images:
				opt = {
					'owner': self.context['db_model'].owner,
					'group': self.context['db_model'],
					'url': image['image_path'],
					'width': image['width'],
					'height': image['height'],
					'title': image['title']
				}
				image = Image()
				image.save(opt)

	def create(self, owner_id, name, images=None):
		'''
		创建图片分组
		'''
		image_group = self.__save(owner_id, name)
		if images:
			for image in images:
				opt = {
					'owner': owner_id,
					'group': image_group.id,
					'url': image['image_path'],
					'width': image['width'],
					'height': image['height'],
					'title': image['title']
				}
				image = Image()
				image.save(opt)
		return ImageGroup(image_group)




