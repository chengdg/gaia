# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from business.mall.corporation import Corporation
from db.account import models as account_model


class CorporationRepository(business_model.Model):
	def filter_corps(self, args=None, page_info=None):
		args = args if args else {}
		company_name = args.get('company_name')
		username = args.get('username')
		is_weizoom_corp = args.get('is_weizoom_corp')
		status = args.get('status')

		db_models = account_model.UserProfile.select()
		corps = []
		for model in db_models:
			corp = Corporation(model.user_id)
			if company_name and not company_name in corp.details.company_name:
				continue
			if username and not company_name in corp.details.company_name:
				continue
			if not is_weizoom_corp == None and not bool(int(is_weizoom_corp)) == corp.is_weizoom_corp():
				continue
			if not status == None and not status == int(status):
				continue
			corps.append(corp)

		if page_info:
			page_info, corps = paginator.paginate(corps, page_info.cur_page, page_info.count_per_page)

		return page_info, corps

	def get_corps(self):
		self.filter_corps()