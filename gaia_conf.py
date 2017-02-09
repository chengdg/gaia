# coding: utf8

# 缓存key
CACHE_KEY = {

}

# 消息队列topic
TOPIC = {
	'product': 'test-topic',
	'order': 'test-topic',
	'delivery_item': 'test-topic',
	'mall_config': "test-topic",
	'base_service': 'test-topic',  # 基础的异步化服务，如邮件，模板消息等
	'notify': 'test-topic'  # 短信消息
}

# 消息队列message_name
MESSAGE_NAME = {
	'save_product': 'zeus_save_product'
}
