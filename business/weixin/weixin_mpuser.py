# -*- coding: utf-8 -*-

from business import model as business_model
from db.weixin import models as weixin_models

class WeixinMpuser(business_model.Model):
	"""
	weixin_mpuser
	"""
	__slots__ = (

		# 基本数据
		'id',
		'owner_id',
		'username',
		'is_certified',
		'is_active',
		'created_at'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)
