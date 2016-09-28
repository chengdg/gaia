# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class FreePostageConfig(business_model.Model):
	"""
	免运费配置
	"""
	__slots__ = (
		'id',
		'condition',
		'condition_value',
		'destinations'
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)
			self.destinations = model.destination