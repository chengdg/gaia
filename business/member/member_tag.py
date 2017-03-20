# -*- coding: utf-8 -*-
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

DEFAULT_TAG_NAME = u'未分组'

class MemberTag(business_model.Model):
	"""
	会员标签
	"""
	__slots__ = (
		'id',
		'name'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)
		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)

	def update(self, args):
		"""
		更新
		"""
		member_models.MemberTag.update(name=args['name']).dj_where(id=self.id).execute()

	def tag_members(self, member_ids):
		"""
		为member_ids指定的会员集合打上标签
		"""
		member_models.MemberHasTag.delete().dj_where(member_id__in=member_ids).execute()
		for member_id in member_ids:
			member_models.MemberHasTag.create(
				member = member_id,
				member_tag = self.id
			)

	def tag_member(self, member_id):
		"""
		为member_id指定的会员打上标签
		"""
		return self.tag_members([member_id])

	@cached_context_property
	def member_count(self):
		return member_models.MemberHasTag.select().dj_where(member_tag_id=self.id).count()

	@staticmethod
	def create_default_member_tag_for_corp(corp):
		"""
		创建默认的会员标签：'未分组'
		"""
		if member_models.MemberTag.select().dj_where(webapp_id=corp.webapp_id, name=DEFAULT_TAG_NAME).count() == 0:
			CorporationFactory.set(corp)
			return MemberTag.create({
				'name': DEFAULT_TAG_NAME
			})

	@staticmethod
	def create(args):
		"""
		创建会员等级
		"""
		corp = CorporationFactory.get()
		model = member_models.MemberTag.create(
			webapp_id = corp.webapp_id,
			name = args['name']
		)

		return MemberTag(model)