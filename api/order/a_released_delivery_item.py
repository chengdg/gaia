# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.release_delivery_item_resource import ReleaseDeliveryItemResourceService


class AReleasedDeliveryItem(api_resource.ApiResource):
	"""
	释放的订单，即释放订单资源
	"""
	app = 'order'
	resource = 'released_delivery_item'

	@param_required(['id', 'corp', 'from_status', 'to_status'])
	def put(args):
		release_delivery_item_service = ReleaseDeliveryItemResourceService.get(args['corp'])
		release_delivery_item_service.release(args['id'], args['from_status'], args['to_status'])

		return {}
