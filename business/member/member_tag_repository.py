# -*- coding: utf-8 -*-
from eaglet.core import paginator
from eaglet.core import watchdog

from business.common.page_info import PageInfo
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.member.member_tag import MemberTag

from db.member import models as member_models


class MemberTagRepository(business_model.Service):
	def get_member_tags(self):
		"""
		获得corp中的所有MemberTag对象
		"""
		db_models = member_models.MemberTag.select().dj_where(webapp_id=self.corp.webapp_id)

		return [MemberTag(db_model) for db_model in db_models]

	def get_member_tag_by_id(self, id):
		"""
		根据id获得member tag对象
		"""
		model = member_models.MemberTag.select().dj_where(webapp_id=self.corp.webapp_id, id=id).get()

		return MemberTag(model)

	def delete_member_tag(self, id):
		"""
		删除id指定的会员标签
		"""
		#TODO: 使用RegradeMemberService进行会员重新分级
		member_models.MemberTag.delete().dj_where(webapp_id=self.corp.webapp_id, id=id).execute()

		return True

