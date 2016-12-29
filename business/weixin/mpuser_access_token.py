# -*- coding: utf-8 -*-

from business import model as business_model
from db.weixin import models as weixin_models

class MpuserAccessToken(business_model.Model):
	"""
	access_token
	"""
	__slots__ = (

		# 基本数据
		'id',
		'mpuser_id',
		'access_token',
		'app_id',
		'app_secret',
		'created_at',
		'is_active'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)
