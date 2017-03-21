# -*- coding: utf-8 -*-

from bdem import msgutil
from settings import MODE

if MODE == 'deploy':
	UUID = 317014264
else:
	UUID = 80035247 #钉钉发消息测试群

def send_product_change(supplier_id, product_id):
	"""
	商品创建、更新
	"""
	msgutil.send_message('notify', 'pre_product_update_ding', {
		'uuid': UUID,
		'supplier_id': supplier_id,
		'product_id': product_id
	})

def send_reject_product_ding_message(supplier_id, product_id, reason):
	"""
	发送商品驳回的ding talk 消息
	"""
	msgutil.send_message('notify', 'pre_product_reject_ding', {
		'uuid': UUID,
		'supplier_id': supplier_id,
		'product_id': product_id,
		'reason': reason
	})