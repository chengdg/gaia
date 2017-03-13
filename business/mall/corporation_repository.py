# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from business.mall.corporation import Corporation
from db.account import models as account_model


class CorporationRepository(business_model.Model):
	def filter_corps(self, args=None, page_info=None):
		"""
		筛选条件：is_weizoom_corp、status
		"""
		args = args if args else {}
		type = args.get('type')
		status = args.get('status')

		db_models = account_model.UserProfile.select()
		if not type == None:
			db_models = db_models.dj_where(webapp_type=int(type))

		if status and not int(status) == -1:
			db_models = db_models.dj_where(status=int(status))

		corps = []
		for model in db_models:
			corp = Corporation(model.user_id)
			corps.append(corp)

		if page_info:
			page_info, corps = paginator.paginate(corps, page_info.cur_page, page_info.count_per_page)

		return page_info, corps

	def get_corps(self):
		self.filter_corps()