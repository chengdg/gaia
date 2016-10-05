# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.image_group.image_group import ImageGroup

class ImageGroupRepository(business_model.Service):
	"""
	图片分组的Repository
	"""
	def get_image_groups(self):
		image_group_models = mall_models.ImageGroup.select().dj_where(owner_id=self.corp.id)
		image_groups = []
		for model in image_group_models:
			image_groups.append(ImageGroup.from_model({
				'db_model': model
			}))

		return image_groups

	def get_image_group(self, image_group_id):
		model = mall_models.ImageGroup.select().dj_where(id=image_group_id).get()

		if model:
			image_group = ImageGroup.from_model({
				'db_model': model
			})

			image_group.set_corp(self.corp)
			return image_group
		else:
			return None

	def delete_image_group(self, image_group_id):
		mall_models.Image.delete().dj_where(owner_id=self.corp.id, group_id=image_group_id).execute()
		mall_models.ImageGroup.delete().dj_where(owner_id=self.corp.id, id=image_group_id).execute()
