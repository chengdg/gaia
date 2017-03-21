# -*- coding: utf-8 -*-

from bdem import msgutil
from settings import MODE

if MODE == 'deploy1':
	UUID = 317014264
	DING_TOPIC = 'notify'
	PRODUCT_OUTGIVING_TOPIC = 'test_topic'
else:
	UUID = 80035247 #钉钉发消息测试群
	DING_TOPIC = 'test-phone'
	PRODUCT_OUTGIVING_TOPIC = 'test_topic'

def send_product_change(supplier_id, product_id):
	"""
	商品创建、更新
	"""
	msgutil.send_message(DING_TOPIC, 'pre_product_update_ding', {
		'uuid': UUID,
		'supplier_id': supplier_id,
		'product_id': product_id
	})
	print supplier_id, 'send_product_change...', product_id

def send_reject_product_ding_message(supplier_id, product_id, reason):
	"""
	发送商品驳回的ding talk 消息
	"""
	msgutil.send_message(DING_TOPIC, 'pre_product_reject_ding', {
		'uuid': UUID,
		'supplier_id': supplier_id,
		'product_id': product_id,
		'reason': reason
	})

	print supplier_id, 'send_reject_product_ding_message...', product_id

def send_product_outgiving_message(corp_id, product_id):
	msgutil.send_message(PRODUCT_OUTGIVING_TOPIC, 'outgiving_product', {
		'corp_id': corp_id,
		'product_id': product_id
	})

	print corp_id, 'send_outgiving_product_message...', product_id