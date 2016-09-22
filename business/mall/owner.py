# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class Owner(business_model.Model):
	"""
	云商通系统中的webapp_owner
	"""

	__slots__ = (
		'id',
		'username',
		'mall_type',
		'config',
		'store_name',
		'webapp_id'
	)

	def __init__(self, owner_id):
		_user = account_model.User.select().dj_where(id=owner_id).first()
		_user_profile = account_model.UserProfile.select().dj_where(user_id=owner_id).first()

		self.id = owner_id
		self.username = _user.username
		self.mall_type = _user_profile.webapp_type
		self.store_name = _user_profile.store_name
		self.webapp_id = _user_profile.webapp_id
