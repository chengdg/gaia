# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource

from business import model as business_model
from db.account import account_repository as account
from user_profile import UserProfile

class User(business_model.Model):
	"""
	用户
	"""
	__slots__ = (
		'id',
		'is_superuser',
		'username',
		'first_name',
		'last_name',
		'email',
		'is_staff',
		'is_active',
		'date_joined',
	)

	def __init__(self, owner_id):
		business_model.Model.__init__(self)
		user_db_model = account.User(owner_id)
		self.context['model'] = user_db_model
		self._init_slot_from_model(user_db_model)
		
		profile = self.context['model'].get_profile()
		self.context['profile'] = UserProfile(profile)

	def get_profile(self):
		return self.context['profile']