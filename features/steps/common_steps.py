# -*- coding: utf-8 -*-
#import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

import logging

from features.util import http

class Corporation(object):
	def __init__(self, id):
		self.id = id


@given(u"{user}登录系统")
def step_impl(context, user):
	user = account_models.User.get(username=user)
	#profile = account_models.UserProfile.get(user=user.id)
	client = bdd_util.login(user)
	
	context.client = client
	context.corp = Corporation(user.id)