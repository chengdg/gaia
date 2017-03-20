# -*- coding: utf-8 -*-
import json
from bs4 import BeautifulSoup
import math
import itertools
import uuid
import time
import random
import string

from eaglet.decorator import param_required
from db.member import models as member_models
from business import model as business_model 
import settings
from eaglet.decorator import cached_context_property
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business.mall.corporation_factory import CorporationFactory

class IntegralLog(business_model.Model):
	"""
	会员积分日志
	"""
	__slots__ = (
		'id',
		'event',
		'integral_increment',
		'reason',
		'current_integral',
		'actor',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.event = member_models.INTEGRALLOGTYPE2STR[model.event_type]
			self.integral_increment = model.integral_count
			self.actor = model.manager

	@cached_context_property
	def related_member(self):
		if self.event == 'recommend_follow' or self.event == 'recommend_purchase':
			corp = CorporationFactory.get()
			db_model = self.context['db_model']
			if db_model.follower_member_token:
				member = corp.member_repository.get_member_by_token(db_model.follower_member_token)
				if member:
					if member and member.thumbnail and member.thumbnail != '':
						return {
							'pic': member.thumbnail,
							'name': member.username_size_ten
						}
					else:
						return None
			else:
				return None
		else:
			return None

	@staticmethod
	def create(corp, event, member, integral_increment, new_integral, reason):
		event_type = member_models.INTEGRALLOGTYPE2VALUE.get(event, member_models.MANAGER_MODIFY)
		model = member_models.MemberIntegralLog.create(
			member = member.id,
			follower_member_token = '',
			integral_count = integral_increment,
			event_type = event_type,
			webapp_user_id = member.webapp_user_id,
			reason = reason,
			current_integral = new_integral,
			manager = corp.username
		)

		return IntegralLog(model)
