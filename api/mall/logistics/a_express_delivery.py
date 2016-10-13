# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.express_delivery import ExpressDelivery
from business.mall.logistics.express_delivery_repository import ExpressDeliveryRepository


class AExpressDelivery(api_resource.ApiResource):
	app = 'mall'
	resource = 'express_delivery'

	@param_required(['corp_id', 'company_id'])
	def put(args):
		'''
		创建物流公司
		'''
		express_delivery = ExpressDelivery.create({
			'company_id': args['company_id'],
			'remark': args.get('remark', '')
		})
		return {}

	@param_required(['corp_id', 'id', 'company_id', 'remark'])
	def post(args):
		corp = args['corp']
		express_delivery = corp.express_delivery_repository.get_express_delivery(args['id'])
		express_delivery.update(args['company_id'], args['remark'])

		return {}

	@param_required(['corp_id', 'id'])
	def delete(args):
		corp = args['corp']
		corp.express_delivery_repository.delete_express_delivery(args['id'])
		
		return {}

