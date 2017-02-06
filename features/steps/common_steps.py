# -*- coding: utf-8 -*-

from behave import *
from features.util import bdd_util
from db.account import models as account_models

class Corporation(object):
	def __init__(self, id):
		self.id = id

	@property
	def is_weizoom_corp(self):
		_account_user_profile = account_models.UserProfile.select().dj_where(user_id=self.id).first()
		return _account_user_profile.webapp_type == account_models.WEBAPP_TYPE_WEIZOOM


@given(u"{user}登录系统")
def step_impl(context, user):
	user = account_models.User.get(username=user)
	#profile = account_models.UserProfile.get(user=user.id)
	client = bdd_util.login(user)
	
	context.client = client
	context.corp = Corporation(user.id)