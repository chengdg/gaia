# -*- coding: utf-8 -*-

from business import model as business_model
from db.weixin import models as weixin_models
from datetime import datetime, timedelta

class WeixinNews(business_model.Model):
	"""
	图文消息
	"""
	__slots__ = (

		# 基本数据
		'id',
		'material_id',
		'title'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)
