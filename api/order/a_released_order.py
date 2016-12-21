# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.release_order_resource_service import ReleaseOrderResourceService


class AReleasedOrder(api_resource.ApiResource):
	"""
	释放的订单，即释放订单资源
	"""
	app = 'order'
	resource = 'released_order'

	@param_required(['id', 'corp', 'from_status', 'to_status'])
	def put(args):
		release_order_resource_service = ReleaseOrderResourceService.get(args['corp'])
		release_order_resource_service.release(args['id'], args['from_status'], args['to_status'])

		return {}
