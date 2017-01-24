# -*- coding: utf-8 -*-

from eaglet.core import api_resource

from business.common.page_info import PageInfo
from business.mall.corporation_repository import CorporationRepository


class ACorps(api_resource.ApiResource):
	"""
	账户列表
	"""
	app = 'account'
	resource = 'corps'

	def get(args):
		page_info = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		page_info, corps = CorporationRepository().filter_corps(args, page_info)

		print corps

		rows = [{
			'corp_id': corp.id,
			'name': corp.details.name,
			'company_name': corp.details.company_name,
			'username': corp.username,
			'is_weizoom_corp': corp.is_weizoom_corp(),
			'max_product_count': corp.details.max_product_count,
			'classification_ids': corp.details.classification_ids,
			'purchase_method': corp.details.purchase_method,
			'points': corp.details.points,
			'clear_period': corp.details.clear_period,
			'contact': corp.details.contact,
			'contact_phone': corp.details.contact_phone,
			'created_at': corp.details.created_at.strftime('%Y-%m-%d %H:%M:%S') if corp.details.created_at else '',
		} for corp in corps]

		return {
			'rows': rows,
			'pageinfo': page_info.to_dict()
		}
