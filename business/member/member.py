# -*- coding: utf-8 -*-
"""@package business.account.member
会员
"""

import re
import json
import math
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from bdem import msgutil

from eaglet.decorator import param_required
from eaglet.decorator import cached_context_property
from eaglet.utils.string_util import hex_to_byte, byte_to_hex
from eaglet.core import watchdog

import settings
from business.account.integral import Integral
from gaia_conf import TOPIC
from util import emojicons_util
from db.member import models as member_models
from business import model as business_model
from business.member.member_has_tag import MemberHasTag
from db.mall import models as mall_models
from business.mall.corporation_factory import CorporationFactory


class Member(business_model.Model):
	"""
	会员
	"""
	__slots__ = (
		'id',
		'username_hexstr',
		# 'webapp_user',
		'is_subscribed',
		'created_at',
		'token',
		'webapp_id',
		'pay_money',
		'update_time',
		'status',
		'experience',
		'remarks_name',
		'remarks_extra',
		'last_visit_time',
		'session_id',
		'is_subscribed',
		'friend_count',
		'factor',
		'source',
		'integral',
		'update_time',
		'pay_times',
		'last_pay_time',
		'unit_price',
		'city',
		'province',
		'country',
		'sex',
		'purchase_frequency',
		'cancel_subscribe_time',
		'fans_count'
	)

	# @staticmethod
	# @param_required(['models'])
	# def from_models(args):
	# 	"""
	# 	工厂对象，根据member model获取Member业务对象

	# 	@param[in] model: member model

	# 	@return Member业务对象
	# 	"""
	# 	models = args['models']
	# 	corp = args['corp']
	# 	members = []
	# 	for model in models:
	# 		member = Member(model)
	# 		member.context['corp'] = corp
	# 		member.context['db_model'] = model
	# 		members.append(member)
	# 	return members

	def __init__(self, model):
		business_model.Model.__init__(self)

		# self.context['webapp_owner'] = webapp_owner
		self.context['db_model'] = model
		self.context['corp'] = CorporationFactory.get()
		if model:
			self._init_slot_from_model(model)

	@cached_context_property
	def webapp_user_id(self):
		return member_models.WebAppUser.select().dj_where(member_id=self.id).first().id

	def increase_integral_after_finish_order(self, order):
		"""
		有用
		@param order:
		@return:
		"""
		Integral.increase_after_order_payed_finsh({
			'member': self,
			'order': order,
			'corp': self.context['corp']
		})

	def cleanup_cache(self):
		"""
		有用
		@return:
		"""
		openid = member_models.MemberHasSocialAccount.select().dj_where(member_id=self.id).first().account.openid
		# 先暂时使用mall_config主题，目的是为了省两块钱TODO
		topic_name = TOPIC['mall_config']
		msg_name = 'member_info_updated'
		data = {
			"weapp_id": self.webapp_id,
			"openid": openid
		}
		msgutil.send_message(topic_name, msg_name, data)

	def update_pay_info(self, order, from_status, to_status):
		"""
		有用
		@param order:
		@param from_status:
		@param to_status:
		@return:
		"""
		if to_status == 'paid':
			last_pay_time = order.payment_time
		else:
			last_pay_time = self.last_pay_time

		webapp_user_id = order.webapp_user_id

		pay_money = 0
		pay_times = 0

		user_orders = self.context['corp'].order_repository.get_orders_by_webapp_user_id(webapp_user_id,
		                                                                                 mall_models.ORDER_STATUS_SUCCESSED)

		for user_order in user_orders:
			pay_money += user_order.pay_money
			pay_times += 1

		if pay_times > 0:
			unit_price = pay_money / pay_times
		else:
			unit_price = 0

		member_models.Member.update(unit_price=unit_price, pay_times=pay_times,
		                            pay_money=pay_money,
		                            last_pay_time=last_pay_time).dj_where(
			id=self.id).execute()

	def auto_update_grade(self):
		"""
		@param corp:
		@param member:
		@param delete:
		@return:是否改变了等级
		"""

		db_model = self.context['db_model']
		member_grades = self.context['corp'].member_grade_repository.get_auto_upgrade_for_corp()

		member_grades = filter(lambda x: x.id > db_model.grade_id, member_grades)

		user_orders = self.context['corp'].order_repository.get_orders_by_webapp_user_id(self.webapp_user_id,
		                                                                                 mall_models.ORDER_STATUS_SUCCESSED)

		pay_money = 0
		pay_times = 0
		for user_order in user_orders:
			pay_money += user_order.pay_money
			pay_times += 1

		is_all_conditions = self.context['corp'].mall_config_repository.get_integral_strategy().is_all_conditions

		new_grade = None
		for grade in member_grades:
			if is_all_conditions:
				if pay_money >= grade.pay_money and pay_times >= grade.pay_times:
					new_grade = grade
			else:
				if pay_money >= grade.pay_money or pay_times >= grade.pay_times:
					new_grade = grade

			if new_grade:
				member_models.Member.update(grade=new_grade.id).dj_where(id=self.id).execute()
				break

	@property
	def discount(self):
		"""
		[property] 会员折扣

		@return 返回二元组(grade_id, 折扣百分数)
		"""
		member_model = self.context['db_model']
		if not member_model:
			return -1, 100

		member_grade = self.__grade
		if member_grade:
			return member_model.grade_id, member_grade.shop_discount
		else:
			return member_model.grade_id, 100

	@cached_context_property
	def grade(self):
		"""
		[property] 会员等级
		"""
		db_model = self.context['db_model']
		corp = CorporationFactory.get()
		grade_id = db_model.grade_id
		return corp.member_grade_repository.get_member_grade_by_id(grade_id)

	@property
	def grade_name(self):
		"""
		[property] 会员等级名称
		"""
		return self.__grade.name

	@cached_context_property
	def tags(self):
		"""
		[property] 会员分组信息列表
		"""
		member_model = self.context['db_model']
		if not member_model:
			return None

		member_tag_ids = [relation.member_tag_id for relation in member_models.MemberHasTag.select().dj_where(member_id=self.id)]
		corp = CorporationFactory.get()

		if len(member_tag_ids) == 0:
			#如果没有标签，默认打上'未分组'标签
			default_tag = corp.member_tag_repository.get_default_member_tag()
			member_models.MemberHasTag.create(
				member = self.id,
				member_tag = default_tag.id
			)
			return [default_tag]
		else:
			return corp.member_tag_repository.get_member_tags_by_ids(member_tag_ids)

	@cached_context_property
	def __info(self):
		"""
		[property] 与会员对应的MemberInfo model对象
		"""
		member_model = self.context['db_model']
		if not member_model:
			return None

		try:
			member_info = member_models.MemberInfo.get(member=member_model)
		except:
			member_info = member_models.MemberInfo()
			member_info.member = member_model
			member_info.name = ''
			member_info.weibo_name = ''
			member_info.phone_number = ''
			member_info.sex = member_models.SEX_TYPE_UNKOWN
			member_info.is_binded = False
			member_info.weibo_nickname = ''
			member_info.phone_number = ''
			member_info.save()

		if member_info.phone_number and len(member_info.phone_number) > 10:
			member_info.phone = '%s****%s' % (member_info.phone_number[:3], member_info.phone_number[-4:])
		else:
			member_info.phone = ''

		return member_info

	@property
	def phone(self):
		"""
		[property] 会员绑定的手机号码加密
		"""

		return self.__info.phone

	@cached_context_property
	def phone_number(self):
		"""
		[property] 会员绑定的手机号码
		"""

		return self.__info.phone_number

	@cached_context_property
	def captcha(self):
		"""
		[property] 手机验证码
		"""
		return self.__info.captcha

	@cached_context_property
	def captcha_session_id(self):
		"""
		[property] 手机验证码
		"""
		return self.__info.session_id

	@property
	def name(self):
		"""
		[property] 会员名
		"""

		return self.__info.name

	@property
	def is_binded(self):
		"""
		[property] 会员是否进行了绑定
		"""
		return self.__info.is_binded

	@cached_context_property
	def user_icon(self):
		"""
		[property] 会员头像
		"""
		return self.context['db_model'].user_icon

	@cached_context_property
	def username_for_html(self):
		"""
		[property] 兼容html显示的会员名
		"""
		if (self.username_hexstr is not None) and (len(self.username_hexstr) > 0):
			username = emojicons_util.encode_emojicons_for_html(self.username_hexstr, is_hex_str=True)
		else:
			username = emojicons_util.encode_emojicons_for_html(self.username)

		try:
			username.decode('utf-8')
		except:
			username = self.username_hexstr

		return username

	@cached_context_property
	def market_tools(self):
		"""
		[property] 会员参与的营销工具集合
		"""
		# TODO2: 实现营销工具集合
		print u'TODO2: 实现营销工具集合'
		return []

	@staticmethod
	def empty_member():
		"""工厂方法，创建空的member对象

		@return Member对象
		"""
		member = Member(None, None)
		return member

	@property
	def username(self):
		return hex_to_byte(self.username_hexstr)

	@cached_context_property
	def username_size_ten(self):
		try:
			username = unicode(self.username_for_html, 'utf8')
			_username = re.sub('<[^<]+?><[^<]+?>', ' ', username)
			if len(_username) <= 10:
				return username
			else:
				name_str = username
				span_list = re.findall(r'<[^<]+?><[^<]+?>', name_str)  # 保存表情符

				output_str = ""
				count = 0

				if not span_list:
					return u'%s...' % name_str[:10]

				for span in span_list:
					length = len(span)
					while not span == name_str[:length]:
						output_str += name_str[0]
						count += 1
						name_str = name_str[1:]
						if count == 10:
							break
					else:
						output_str += span
						count += 1
						name_str = name_str[length:]
						if count == 10:
							break
					if count == 10:
						break
				return u'%s...' % output_str
		except:
			return self.username_for_html[:10]

	def join_groups(self, group_ids):
		"""
		加入group_id指定的会员分组
		即
		将会员打上group_ids指定的member tag
		"""
		if len(group_ids) == 0:
			#退出所有会员分组，回到默认的'未分组'
			corp = CorporationFactory.get()
			default_tag = corp.member_tag_repository.get_default_member_tag()
			member_models.MemberHasTag.create(
				member = self.id,
				member_tag = default_tag.id
			)
			return 1
		else:
			member_models.MemberHasTag.delete().dj_where(member_id=self.id).execute()
			tag_ids = group_ids
			count = 1
			for tag_id in tag_ids:
				member_models.MemberHasTag.create(
					member = self.id,
					member_tag = tag_id
				)
				count += 1

			return count
