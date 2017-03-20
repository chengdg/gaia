# -*- coding: utf-8 -*-

from business import model as business_model
from business.member.member import Member
from db.member import models as member_models
from eaglet.core import paginator
from db.account import models as account_models


class MemberFactory(business_model.Service):
	def create_member(self, username, openid):
		pass
