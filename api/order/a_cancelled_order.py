# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required



class ACancelledOrder(api_resource.ApiResource):
	"""
	已取消的订单
	"""
	app = "order"
	resource = "cancelled_order"

	@param_required(['id'])
	def put(args):
		"""
		取消订单
		@return:
		"""
		corp = args['corp']
		id = args['id']

		order_repository = corp.order_repository
		order = order_repository.get_order(id)
		if order:
			is_success, msg = order.cancel(corp)
			if is_success:
				return {}
			else:
				return 500, {'msg': msg}
		else:
			return 500, {}
