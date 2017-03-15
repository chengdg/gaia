# -*- coding: utf-8 -*-

from db.member import models as member_models
from eaglet.core import paginator
from db.account import models as account_models

from business import model as business_model
from business.member.member import Member
from business.member.integral_log import IntegralLog


class ModifyMemberService(business_model.Service):
	"""
	更新会员信息的service
	"""
	
	def update_grade_for_members(self, member_ids, member_grade_id):
		"""
		将member_ids中指定的会员的等级修改为member_grade_id指定的会员等级
		"""
		grades = list(member_models.MemberGrade.select().dj_where(webapp_id=self.corp.webapp_id, id=member_grade_id))
		if len(grades) == 0:
			return False

		target_grade = grades[0]
		member_models.Member.update(grade=target_grade.id).dj_where(webapp_id=self.corp.webapp_id, id__in=member_ids).execute()
		return True	

	def add_integral(self, member_id, integral_increment, reason):
		"""
		为member增加积分
		"""
		#为member增加积分
		member = self.corp.member_repository.get_member_by_id(member_id)
		new_integral = member.integral + integral_increment
		member_models.Member.update(integral=new_integral).dj_where(id=member_id).execute()

		#记录积分日志
		if integral_increment > 0:
			event = 'manager_modify_increase'
		else:
			event = 'manager_modify_decrease'
		IntegralLog.create(self.corp, event, member, integral_increment, new_integral, reason)