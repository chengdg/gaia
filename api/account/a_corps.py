# -*- coding: utf-8 -*-

from eaglet.core import api_resource

from business.mall.corporation_repository import CorporationRepository


class ACorps(api_resource.ApiResource):
	"""
	账户列表
	"""
	app = 'account'
	resource = 'corps'

	def get(args):
		corps = CorporationRepository().get_corps()

		return [{
			'corp_id': corp.id,
			'corp_name': corp.details.name,
			'username': corp.details.username,
			'type': corp.type,
			'max_product_count': corp.details.max_product_count,
			'purchase_method': corp.details.purchase_method,
			'points': corp.details.points,
			'clear_period': corp.details.clear_period,
			'contact': corp.details.contact,
			'contact_phone': corp.details.contact_phone,
			'valid_time_from': corp.details.valid_time_from,
			'valid_time_to': corp.details.valid_time_to
		} for corp in corps]
