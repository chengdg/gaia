# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class ACorp(api_resource.ApiResource):
	"""
	账户配置
	"""
	app = 'account'
	resource = 'corp'

	@param_required(['corp_id'])
	def get(args):

		corp = args['corp']

		return {
			'corp_id': corp.id,
			'corp_name': corp.details.name,
			'username': corp.username,
			'type': corp.type,
			'max_product_count': corp.details.max_product_count,
			'classification_ids': corp.details.classification_ids,
			'purchase_method': corp.details.purchase_method,
			'points': corp.details.points,
			'clear_period': corp.details.clear_period,
			'contact': corp.details.contact,
			'contact_phone': corp.details.contact_phone,
			'valid_time_from': corp.details.valid_time_from,
			'valid_time_to': corp.details.valid_time_to,
			'note': corp.details.note,
			'customer_from': corp.details.customer_from,
			'status': corp.details.status,
			'created_at': corp.details.created_at,
			'pre_sale_tel': corp.details.pre_sale_tel,
			'after_sale_tel': corp.details.after_sale_tel,
			'service_tel': corp.details.service_tel,
			'service_qq_first': corp.details.service_qq_first,
			'service_qq_second': corp.details.service_qq_second
		}

	@param_required(['corp_id', 'is_weizoom_corp:bool'])
	def post(args):
		corp = args['corp']
		corp.update(args)

		return {}