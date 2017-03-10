# -*- coding: utf-8 -*-

from business import model as business_model
from business.member.member import Member
from db.member import models as member_models


class MemberRepository(business_model.Service):
	def get_member_by_id(self, member_id):
		member_db_model = member_models.Member.get(webapp_id=self.corp.webapp_id, id=member_id)

		return Member(member_db_model)

	def get_members_from_webapp_user_ids(self, webapp_user_ids):
		"""
		根据webapp_user_ids获得member集合
		"""
		webappuser_id2member = dict(
			[(u.id, u.member_id) for u in member_models.WebAppUser.select().dj_where(id__in=webapp_user_ids)])
		member_ids = webappuser_id2member.values()
		db_member_models = member_models.Member.select().dj_where(id__in=member_ids)

		members = [Member(db_member_model) for db_member_model in db_member_models]
		id2member = dict([(m.id, m) for m in members])

		for webapp_user_id, member_id in webappuser_id2member.items():
			webappuser_id2member[webapp_user_id] = id2member.get(member_id, None)

		return webappuser_id2member, members
