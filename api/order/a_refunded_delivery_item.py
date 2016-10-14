# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ARefundedDeliveryItem(api_resource.ApiResource):
	"""
	已支付的订单
	"""
	app = 'order'
	resource = 'refunded_delivery_item'

	@param_required(['delivery_item_id', 'corp'])
	def put(args):
		"""
		支付订单
		@return:
		"""
		corp = args['corp']
		delivery_item_id = args['delivery_item_id']

		delivery_item_repository = corp.delivery_item_repository
		delivery_item = delivery_item_repository.get_delivery_item(delivery_item_id)
		if delivery_item:
			is_success, msg = delivery_item.refund(corp)
			if is_success:
				return {}
			else:
				return 500, {'msg': msg}
		else:
			return 500, {}
