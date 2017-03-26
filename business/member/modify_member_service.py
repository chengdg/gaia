# -*- coding: utf-8 -*-

from db.member import models as member_models
from eaglet.core import paginator
from db.account import models as account_models

from business import model as business_model
from business.member.member import Member
from business.member.integral_log import IntegralLog
from business.member.member_ship_info import MemberShipInfo
from business.common.encode_district_service import EncodeDistrictService


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

	def update_basic_member_info(self, member_id, basic_member_info):
		"""
		更新会员的基本信息
		"""
		member_options = {}
		member_info_options = {}
		if 'phone_number' in basic_member_info:
			member_info_options['phone_number'] = basic_member_info['phone_number']

		sex2value = {
			'male': member_models.SEX_TYPE_MEN,
			'female': member_models.SEX_TYPE_WOMEN,
			'unknown': member_models.SEX_TYPE_UNKOWN
		}
		if 'sex' in basic_member_info:
			sex_value = sex2value[basic_member_info['sex']]
			member_options['sex'] = sex_value
			member_info_options['sex'] = sex_value

		if 'remark' in basic_member_info:
			member_options['remarks_extra'] = basic_member_info['remark']

		if 'remark_name' in basic_member_info:
			member_options['remarks_name'] = basic_member_info['remark_name']

		if member_options:
			member_models.Member.update(**member_options).dj_where(webapp_id=self.corp.webapp_id, id=member_id).execute()

		if member_info_options:
			member_models.MemberInfo.update(**member_info_options).dj_where(member_id=member_id).execute()	

	def add_ship_info(self, member_id, data):
		"""
		为member增加发货信息
		"""
		member = self.corp.member_repository.get_member_by_id(member_id)
		area = data.get('area', None)
		area_code = EncodeDistrictService.get().encode(area)

		is_selected = data.get('is_selected', False)
		if is_selected:
			member_models.ShipInfo.update(is_selected=0).dj_where(webapp_user_id=member.webapp_user_id).execute()

		db_model = member_models.ShipInfo.create(
			webapp_user_id = member.webapp_user_id,
			ship_tel = data.get('phone', ''),
			ship_address = data.get('address', ''),
			ship_name = data.get('receiver_name', ''),
			area = area_code,
			is_selected = is_selected
		)

		return MemberShipInfo(db_model)