# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation import Corporation


class ACorp(api_resource.ApiResource):
	"""
	账户配置
	"""
	app = 'account'
	resource = 'corp'

	@param_required(['corp_id'])
	def get(args):

		corp = Corporation(args['corp_id'])

		return {
			'corp_id': corp.id,
			'name': corp.details.name,
			'company_name': corp.details.company_name,
			'username': corp.username,
			'type': corp.type,
			'corp_type': corp.corp_type,
			'is_weizoom_corp': corp.is_weizoom_corp(),
			'max_product_count': corp.details.max_product_count,
			'classification_ids': corp.details.classification_ids,
			'settlement_type': corp.details.settlement_type,
		   	'divide_rebate': corp.details.divide_rebate,
			'clear_period': corp.details.clear_period,
			'axe_sales_name': corp.details.axe_sales_name,
			'status': corp.details.status
		}