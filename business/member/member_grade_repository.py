# -*- coding: utf-8 -*-
"""
会员等级
"""
from eaglet.core import paginator
from eaglet.core import watchdog

from business.common.page_info import PageInfo
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.member.member_grade import MemberGrade
from business.member.social_account import SocialAccount

from db.member import models as member_models


class MemberGradeRepository(business_model.Service):
	def get_auto_upgrade_for_corp(self):
		db_models = member_models.MemberGrade.select().dj_where(webapp_id=self.corp.webapp_id,
		                                                        is_auto_upgrade=True).order_by(
			-member_models.MemberGrade.id)

		return [MemberGrade(db_model) for db_model in db_models]
