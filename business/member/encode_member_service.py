# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from business import model as business_model

class EncodeMemberService(business_model.Service):
	"""
	将Member对象转换为可输出dict的服务
	"""
	def get_basic_info(self, member):
		"""
		获得会员的基础信息
		"""
		return {
			"phone_number": member.phone_number,
			"remark_name": member.remark_name,
			"remark": member.remark,
			"sex": member.sex
		}

	def get_groups_info(self, member):
		"""
		获得会员的分组数据
		"""
		group_datas = []
		for member_tag in member.tags:
			group_datas.append({
				'id': member_tag.id,
				'name': member_tag.name
			})

		return group_datas

	def get_grade_info(self, member):
		"""
		获得会员的等级数据
		"""
		member_grade = member.grade
		return {
			'id': member_grade.id,
			'name': member_grade.name
		}

	def get_consume_info(self, member):
		"""
		获得会员的消费数据
		"""
		return {
			'pay_times': member.pay_times,
			'pay_money': member.pay_money,
			'unit_price': member.unit_price,
			'last_pay_time': member.last_pay_time.strftime('%Y-%m-%d %H:%M') if member.last_pay_time else None,
			'pay_times_in_30_days': member.pay_times_in_30_days,
			'integral': member.integral
		}

	def get_social_info(self, member):
		"""
		获得会员的社交数据
		"""
		return {
			'factor': member.factor,
			'friend_count': member.friend_count,
			'fans_count': member.fans_count,
		}

	def get_subscribe_info(self, member):
		"""
		获得会员的社交数据
		"""
		return {
			'is_subscribed': member.is_subscribed,
			'status': member.status,
			'source': member.source,
			'subscribe_time': '2017-01-01 00:00'
		}

	def encode(self, member):
		pass

	def get_ship_infos(self, member):
		"""
		获得会员的收货地址信息
		"""
		datas = []
		for ship_info in member.ship_infos:
			datas.append({
				'id': ship_info.id,
				'receiver_name': ship_info.receiver_name,
				'phone': ship_info.phone,
				'area_code': ship_info.area_code,
				'area': ship_info.area,
				'address': ship_info.address,
				'is_selected': ship_info.is_selected
			})
		return datas
