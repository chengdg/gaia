# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.encode_delivery_item_service import EncodeDeliveryItemService



class ADeliveryItemPhoneMessageNotification(api_resource.ApiResource):
	"""
	短信发送
	"""
	app = 'delivery_item'
	resource = 'phone_message'

	@param_required(['delivery_item_id'])
	def put(args):
		"""
		短信发送
		"""

		corp = args['corp']
		delivery_item_repository = corp.delivery_item_repository

		delivery_item_id = args['delivery_item_id']
		delivery_item = delivery_item_repository.get_delivery_item(delivery_item_id)

		delivery_item.send_phone_message(corp)
		
		return {}

	
