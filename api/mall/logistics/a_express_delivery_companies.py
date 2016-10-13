# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.express_delivery import ExpressDelivery


class AExpressDeliveryCompanies(api_resource.ApiResource):
	"""
	快递公司集合
	"""
	app = 'mall'
	resource = 'express_delivery_companies'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		companies = []
		for company in corp.express_delivery_repository.get_companies():
			companies.append({
				"id": company.company_id,
				"name": company.name,
				"value": company.value,
				"kdniao_value": company.kdniao_value
			})

		return {
			'companies': companies
		}