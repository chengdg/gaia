# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.express_delivery import ExpressDelivery
from business.mall.logistics.express_delivery_repository import ExpressDeliveryRepository


class AExpressDeliveryDispayIndex(api_resource.ApiResource):
	app = 'mall'
	resource = 'express_delivery_display_index'

	@param_required(['corp_id', 'id', 'direction'])
	def post(args):
		corp = args['corp']
		express_delivery = corp.express_delivery_repository.get_express_delivery(args['id'])
		express_delivery.update_display_index(args['direction'])

		return {}
