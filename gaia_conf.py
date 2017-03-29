# coding: utf8

# coding: utf8
import os
# 消息队列topic
TOPIC = {
	'product': os.environ.get('PRODUCT_TOPIC', 'test-topic'),
	'order': os.environ.get('ORDER_TOPIC', 'test-topic'),
	'delivery_item':  os.environ.get('DELIVERY_ITEM_TOPIC', 'test-topic'),
	'mall_config': os.environ.get('MALL_CONFIG_TOPIC', 'test-topic'),
	'base_service': os.environ.get('BASE_SERVICE_TOPIC', 'test-topic'),  # 基础的异步化服务，如邮件，模板消息等
	'notify': os.environ.get('NOTIFY_TOPIC', 'test-phone')  # 短信消息
}

DING_UUID = {
	'update_product': os.environ.get('UPDATE_PRODUCT_DING_UUID', 80035247),
	'reject_product': os.environ.get('REJECT_PRODUCT_DING_UUID', 80035247)
}