# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator



class PromotionProducts(business_model.Model):
	"""
	促销活动可以选用的商品集合
	"""
	__slots__ = (
	)
	
	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)