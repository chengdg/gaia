# -*- coding: utf-8 -*-

from business import model as business_model
from business.mall.corporation import Corporation
from db.account import models as account_model


class CorporationRepository(business_model.Model):
	def get_corps(self):
		db_models = account_model.UserProfile.select()
		return [Corporation(model.user_id) for model in db_models]