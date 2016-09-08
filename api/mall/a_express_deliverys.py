# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.express_delivery import ExpressDelivery


class AExpressDeliverys(api_resource.ApiResource):
	app = 'mall'
	resource = 'express_deliverys'

	@param_required(['owner_id'])
	def get(args):
		'''
		物流列表
		# 默认排序 -display_index
		'''
		pageinfo, express_deliverys = ExpressDelivery.from_owner_id({'owner_id': args['owner_id'], 'cur_page': args.get('cur_page', 1), 'count_per_page': args.get('count_per_page', 10)})
		
		return {
			'pageinfo': pageinfo.to_dict(),
			'express_deliverys': [express_delivery.to_dict() for express_delivery in express_deliverys]
		}