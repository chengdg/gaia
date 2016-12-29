# -*- coding: utf-8 -*-
import json

from business import model as business_model
from db.mall import models as mall_models


class TemplateMessage(business_model.Model):
	"""
	模板消息
	"""

	__slots__ = (
		'id',
		'industry',
		'title',
		'send_point',
		'attribute',
		'created_at'
	)

	def __init__(self, db_model):

		business_model.Model.__init__(self)
		self.context['db_model'] = db_model
		self._init_slot_from_model(db_model)
			
