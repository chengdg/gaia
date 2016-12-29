# -*- coding: utf-8 -*-
import json

from bdem import msgutil
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class AUnshippedOrdersCount(api_resource.ApiResource):
	app = 'order'
	resource = 'unshipped_orders_count'

	@param_required(['corp'])
	def get(args):
		corp = args['corp']

		unship_orders_count, weixin_unread_count = corp.order_repository.get_unshipped_orders_count()
		return {
			'unship_orders_count': unship_orders_count,
			'weixin_messages_count': weixin_unread_count
		}
