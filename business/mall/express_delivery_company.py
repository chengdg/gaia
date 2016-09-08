# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.express import models as express_models
from core import paginator

from business.mall.image import Image
from core import paginator


class ExpressDeliveryCompany(business_model.Model):
	"""
	物流
	"""
	__slots__ = (
		'id',
		'name',
		'value',
		'kdniao_value'
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)