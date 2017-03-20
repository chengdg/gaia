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

	def get_member_grades(self):
		"""
		获得corp中的所有MemberGrade对象
		"""
		db_models = member_models.MemberGrade.select().dj_where(webapp_id=self.corp.webapp_id)

		return [MemberGrade(db_model) for db_model in db_models]

	def get_member_grade_by_id(self, id):
		"""
		根据id获得member grade对象
		"""
		model = member_models.MemberGrade.select().dj_where(id=id).get()

		return MemberGrade(model)

	def get_upgrade_strategy(self):
		"""
		获取会员等级的升级策略
		会员等级升级策略有两类：
		1. match_all: 全部升级条件都要匹配
		2. match_any: 匹配任一升级条件
		"""
		settings = member_models.IntegralStrategySettings.select().dj_where(webapp_id=self.corp.webapp_id).get()
		if settings.is_all_conditions:
			return 'match_all'
		else:
			return 'match_any'

	def modify_upgrade_strategy(self, strategy):
		"""
		修改会员等级的升级策略
		"""
		if strategy == 'match_all':
			is_all_conditions = True
		else:
			is_all_conditions = False
		member_models.IntegralStrategySettings.update(is_all_conditions=is_all_conditions).dj_where(webapp_id=self.corp.webapp_id).execute()

	def delete_member_grade(self, id):
		"""
		删除id指定的会员等级

		会员等级删除时，要将目前是该会员等级的会员，使用RegradeMemberService进行重新分派等级
		"""
		#TODO: 使用RegradeMemberService进行会员重新分级
		member_models.MemberGrade.delete().dj_where(webapp_id=self.corp.webapp_id, id=id).execute()

		return True

