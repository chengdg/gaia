# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay_interface import PayInterface


class APayInterfaces(api_resource.ApiResource):
	"""
	支付方式列表
	"""
	app = 'mall'
	resource = 'pay_interfaces'

	@param_required(['corp'])
	def get(args):
		corp = args['corp']
		pay_interfaces = corp.pay_interface_repository.get_pay_interfaces()

		datas = []
		for pay_interface in pay_interfaces:
			data = {
				"id": pay_interface.id,
				"type": pay_interface.type,
				"name": pay_interface.name,
				"is_active": pay_interface.is_active,
				"description": pay_interface.description,
				"should_create_related_config": pay_interface.should_create_related_config,
				"configs": []
			}

			datas.append(data)

		return {
			"pay_interfaces": datas
		}
