# -*- coding: utf-8 -*-

from bdem import msgutil

from gaia_conf import TOPIC, DING_UUID

from db.mall import models as mall_models


def send_product_change(supplier_id, product_id):
	"""
	商品创建、更新
	"""
	msgutil.send_message(TOPIC['notify'], 'pre_product_update_ding', {
		'uuid': DING_UUID['update_product'],
		'supplier_id': supplier_id,
		'product_id': product_id
	})
	print supplier_id, 'send_product_change...', product_id

def send_reject_product_ding_message(supplier_id, product_id, reason):
	"""
	发送商品驳回的ding talk 消息
	"""
	msgutil.send_message(TOPIC['notify'], 'pre_product_reject_ding', {
		'uuid': DING_UUID['reject_product'],
		'supplier_id': supplier_id,
		'product_id': product_id,
		'reason': reason
	})

	print supplier_id, 'send_reject_product_ding_message...', product_id

def send_product_outgiving_message(corp_id, product_id):
	msgutil.send_message(TOPIC['product'], 'outgiving_product', {
		'corp_id': corp_id,
		'product_id': product_id
	})

	print corp_id, 'send_outgiving_product_message...', product_id


###############################
#更新缓存消息
###############################
def send_product_created_cache(product_id, product_name):
	"""
	新增商品
	"""
	msgutil.send_message(TOPIC['product'], 'new_product_enter_pool', {
		"product_id": product_id,
		'name': product_name
	})

	print 'send_sync_product_updated_message...', product_id

def send_product_update_cache(product_id):
	"""
	商品更新
	"""
	corp_ids = [p.woid for p in mall_models.ProductPool.select().dj_where(product_id=product_id,
                                                                 status=mall_models.PP_STATUS_ON)]
	msgutil.send_message(TOPIC['product'], 'sync_product_updated', {
		'corp_ids': corp_ids,
		'product_id': product_id
	})

	print 'send_sync_product_updated_message...', product_id
