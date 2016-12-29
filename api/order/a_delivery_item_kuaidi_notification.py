# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.encode_delivery_item_service import EncodeDeliveryItemService
from business.mall.express.express_service import ExpressService


class ADeliveryItemKuaidiNotification(api_resource.ApiResource):
	"""
	快递订阅
	"""
	app = 'delivery_item'
	resource = 'notify_kuaidi'

	@param_required(['delivery_item_id'])
	def put(args):
		"""
		根据出货单订阅快递
		"""

		corp = args['corp']
		delivery_item_repository = corp.delivery_item_repository

		delivery_item_id = args['delivery_item_id']

		delivery_item = delivery_item_repository.get_delivery_item(delivery_item_id)
		if delivery_item.with_logistics_trace:
			# 发送快递订阅
			result = ExpressService(delivery_item).get_express_poll()
		if result:
			return {}
		else:
			return 500, {}

	
