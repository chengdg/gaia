# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""
from business.mall.corporation import Corporation
from service.handler_register import register
from util.send_phone_msg import send_chargeback_message


@register("send_delivery_item_phone_message_task")
def process(data, recv_msg=None):
	# 暂停
	pass
	# corp_id = data['corp_id']
	# delivery_item_id = data['order_id']
	#
	# corp = Corporation(corp_id)
	#
	# delivery_item = corp.delivery_item_repository.get_delivery_item(delivery_item_id)
	#
	# if delivery_item.has_db_record:
	#
	# 	message_content = u"您好，订单号：%s，收货人：%s。已退单，请知晓！【微众传媒】"
	# 	# 获取手机号
	#
	# 	# todo 从出货单读取
	# 	supplier = corp.supplier_repository.get_supplier(delivery_item.supplier_id)
	# 	supplier_tel = supplier.supplier_tel
	#
	# 	if supplier_tel:
	# 		send_chargeback_message(supplier_tel, message_content % (delivery_item.bid, delivery_item.ship_name))

