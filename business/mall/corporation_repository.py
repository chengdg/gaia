# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from business.mall.corporation import Corporation
from db.account import models as account_model


class CorporationRepository(business_model.Model):
	def __get_filter_items(self, args):
		items = dict()
		for item in args:
			if not item.startswith('__f-'):
				continue
			_, field, match_strategy = item.split('-')
			items[field] = args[field]
		return items

	def filter_corps(self, args=None, page_info=None):
		"""
		筛选条件：company_name、is_weizoom_corp、username、status
		"""
		args = args if args else {}
		filter_items = self.__get_filter_items(args)

		company_name = filter_items.get('company_name')
		is_weizoom_corp = filter_items.get('is_weizoom_corp')
		username = filter_items.get('username')
		status = filter_items.get('status')

		db_models = account_model.UserProfile.select()
		corps = []
		for model in db_models:
			corp = Corporation(model.user_id)
			if status and not int(status) == -1 and not int(status) == corp.details.status:
				continue
			if not is_weizoom_corp == None and not int(is_weizoom_corp) == -1 and not bool(int(is_weizoom_corp)) == corp.is_weizoom_corp():
				continue
			if username and not username in corp.username:
				continue
			if company_name and not company_name in corp.details.company_name:
				continue

			corps.append(corp)

		if page_info:
			page_info, corps = paginator.paginate(corps, page_info.cur_page, page_info.count_per_page)

		return page_info, corps

	def get_corps(self):
		self.filter_corps()