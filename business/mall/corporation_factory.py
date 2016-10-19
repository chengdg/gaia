# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from db.account import models as account_model
from business.mall.corporation import Corporation

CORPORATION = None

class CorporationFactory(object):
	@staticmethod
	def set(corporation):
		global CORPORATION
		CORPORATION = corporation

	@staticmethod
	def get():
		global CORPORATION
		return CORPORATION

	@staticmethod
	def get_weizoom_corporation():
		"""
		获得系统中微众对应的公司
		微众对应的公司，其维护了一个统一的可供其他自营平台选择商品的商品池
		"""
		profile = account_model.UserProfile.select().dj_where(webapp_type=account_model.WEBAPP_TYPE_WEIZOOM)[0]

		if profile:
			return Corporation(profile.user_id)
		else:
			return None
