# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

class DivideRebateInfo(business_model.Model):
	"""
	分成模式的信息
	"""
	__slots__ = (
		'id',
		'divide_money', #钱额度
		'basic_rebate', #基础返点
		'rebate' #在此额度内返点
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
