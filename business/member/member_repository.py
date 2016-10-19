# -*- coding: utf-8 -*-

from business import model as business_model
from business.member.member import Member
from db.member import models as member_models


class MemberRepository(business_model.Service):
	def get_member_by_id(self, member_id):
		member_db_model = member_models.Member.get(id=member_id)

		members = Member.from_models({
			'models': member_db_model
		})

		if members:
			return members[0]
		else:
			return None


	def get_members_from_webapp_user_ids(self,webapp_user_ids):
		"""

		@param args:
		@return:
		"""

		webappuser_id2member = dict(
			[(u.id, u.member_id) for u in member_models.WebAppUser.select().dj_where(id__in=webapp_user_ids)])
		member_ids = webappuser_id2member.values()
		db_member_models = member_models.Member.select().dj_where(id__in=member_ids)

		members = Member.from_models({'models': db_member_models})
		id2member = dict([(m.id, m) for m in members])

		for webapp_user_id, member_id in webappuser_id2member.items():
			webappuser_id2member[webapp_user_id] = id2member.get(member_id, None)

		return webappuser_id2member, members