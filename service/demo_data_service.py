# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

import logging
from service.service_register import register

@register("demo_data111")
def demo_order_process(data, recv_msg=None):
	"""
	演示接收消息
	"""

	print('-----data')
	print data
	print('-----data')
	logging.info("data: {}".format(data))
	logging.info("ReceiptHandle: {}".format(recv_msg.receipt_handle))
	logging.info("MessageBody: {}".format(recv_msg.message_body))
	logging.info("MessageID: {}".format(recv_msg.message_id))
	return
