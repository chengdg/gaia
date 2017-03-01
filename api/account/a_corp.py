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
			'is_weizoom_corp': corp.is_weizoom_corp(),
			'max_product_count': corp.details.max_product_count,
			'classification_ids': corp.details.classification_ids,
			'settlement_type': corp.details.settlement_type,
		   	'divide_rebate': corp.details.divide_rebate,
			'clear_period': corp.details.clear_period,
			'contact': corp.details.contact,
			'contact_phone': corp.details.contact_phone,
			'note': corp.details.note,
			'customer_from': corp.details.customer_from,
			'created_at': corp.details.created_at.strftime('%Y-%m-%d %H:%M:%S') if corp.details.created_at else '',
			'status': corp.details.status,
			'pre_sale_tel': corp.details.pre_sale_tel,
			'after_sale_tel': corp.details.after_sale_tel,
			'service_tel': corp.details.service_tel,
			'service_qq_first': corp.details.service_qq_first,
			'service_qq_second': corp.details.service_qq_second
		}

	@param_required(['corp_id'])
	def post(args):
		corp = Corporation(args['corp_id'])
		corp.update(args)

		return {}