# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.express_delivery import ExpressDelivery


class AExpressDeliverys(api_resource.ApiResource):
	app = 'mall'
	resource = 'express_deliveries'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		express_deliveries = corp.express_delivery_repository.get_express_deliveries()

		datas = []
		for express_delivery in express_deliveries:
			datas.append({
				"id": express_delivery.id,
				"name": express_delivery.name,
				"express_number": express_delivery.express_number,
				"express_value": express_delivery.express_value,
				"display_index": express_delivery.display_index,
				'remark': express_delivery.remark
			})

		result = {
			'express_deliveries': datas		
		}

		if 'return_company' in args:
			companies = []
			for company in corp.express_delivery_repository.get_companies():
				companies.append({
					"id": company.company_id,
					"name": company.name,
					"value": company.value,
					"kdniao_value": company.kdniao_value
				})
			result['companies'] = companies

		return result