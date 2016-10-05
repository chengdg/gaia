# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models


class Image(business_model.Model):
	"""
	图片分组
	"""
	__slots__ = (
		'id',
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
	def from_model(model):
		return Image(model)

