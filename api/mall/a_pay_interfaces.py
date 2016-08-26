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

	@param_required(['owner_id'])
	def get(args):
		pay_interfaces = PayInterface.from_owner_id({"owner_id": args['owner_id']})

		pay_interfaces = map(lambda x: x.to_dict('configs'), pay_interfaces)

		return {'pay_interfaces': pay_interfaces}
