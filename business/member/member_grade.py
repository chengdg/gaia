# -*- coding: utf-8 -*-
"""
会员等级
"""

import json
from bs4 import BeautifulSoup
import math
from datetime import datetime

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
from db.member import models as member_models
from eaglet.core import watchdog
from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
import settings
from eaglet.decorator import cached_context_property
from business.mall.corporation_factory import CorporationFactory


DEFAULT_GRADE_NAME = u'普通会员'

class MemberGrade(business_model.Model):
	"""
	会员等级
	"""
	__slots__ = (
		'id',
		'name',
		'is_default_grade',
		'is_auto_upgrade',
		'pay_money',
		'pay_times',
		'shop_discount'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)
		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)

	def update(self, args):
		"""
		更新会员等级
		"""
		member_models.MemberGrade.update(
			name = args['name'],
			is_auto_upgrade = args['is_auto_upgrade'],
			pay_money = args['pay_money'],
			pay_times = args['pay_times'],
			shop_discount = args['shop_discount']
		).dj_where(id=self.id).execute()

	@cached_context_property
	def member_count(self):
		return member_models.Member.select().dj_where(grade_id=self.id).count()

	@staticmethod
	def create_default_member_grade_for_corp(corp):
		if member_models.MemberGrade.select().dj_where(webapp_id=corp.webapp_id, name=DEFAULT_GRADE_NAME).count() == 0:
			return member_models.MemberGrade.create(
				webapp_id = corp.webapp_id,
				name = DEFAULT_GRADE_NAME,
				upgrade_lower_bound = 0,
				is_default_grade = True,
				is_auto_upgrade = True
			)

	@staticmethod
	def create(args):
		"""
		创建会员等级
		"""
		corp = CorporationFactory.get()
		model = member_models.MemberGrade.create(
			webapp_id = corp.webapp_id,
			name = args['name'],
			is_auto_upgrade = args['is_auto_upgrade'],
			pay_money = args.get('pay_money', 0.00),
			pay_times = args.get('pay_times', 0),
			shop_discount = args['shop_discount']
		)

		return MemberGrade(model)