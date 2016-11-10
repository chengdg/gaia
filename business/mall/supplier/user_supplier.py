# -*- coding: utf-8 -*-

from db.account import models as account_models
from business import model as business_model


class UserSupplier(business_model.Model):
	"""
	以weapp.auth_user为供货商，已经不会产生，只在历史订单显示中使用
	"""

	__slots__ = (
		'id',
		'name'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.id = model.id
		self.name = model.store_name

	@staticmethod
	def get_user_supplier_by_user_ids(user_ids):
		db_models = account_models.UserProfile.select().dj_where(user_id__in=user_ids)

		return [UserSupplier(db_model) for db_model in db_models]
