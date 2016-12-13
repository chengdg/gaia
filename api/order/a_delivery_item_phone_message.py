# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.encode_delivery_item_service import EncodeDeliveryItemService
from util.send_phone_msg import send_chargeback_message


class ADeliveryItemPhoneMessage(api_resource.ApiResource):
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
		delivery_item = delivery_item_repository.get_delivery_item(delivery_item_id, {})

		encode_delivery_item_service = EncodeDeliveryItemService.get(corp)
		data = {}
		data.update(encode_delivery_item_service.get_base_info(delivery_item))

		if delivery_item.has_db_record:
		
			message_content = u"您好，订单号：%s，收货人：%s。已退单，请知晓！【微众传媒】"
			# 获取手机号
		
			# 从出货单读取
			supplier = corp.supplier_repository.get_supplier(delivery_item.supplier_id)
			supplier_tel = supplier.supplier_tel
		
			if supplier_tel:
				send_chargeback_message(supplier_tel, message_content % (delivery_item.bid, delivery_item.ship_name))
		
		return {}

	
