# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@Given(u"{username}成为自营平台")
def step_impl(context, username):
	user = account_models.User.get(username=username)
	account_models.UserProfile.update(webapp_type=1).dj_where(user_id=user.id).execute()