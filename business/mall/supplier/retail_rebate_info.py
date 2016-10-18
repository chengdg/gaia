# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

class RetailRebateInfo(business_model.Model):
	"""
	零售返点模式的信息
	"""
	__slots__ = (
		'id',
		'rebate'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def is_belong_to_group_buying(self):
		return self.context['db_model'].owner_id != 0

