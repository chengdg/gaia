# -*- coding: utf-8 -*-
from bdem import msgutil

topic_name = 'test-topic'

for i in xrange(10):
	data = {
		"delivery_item_id": i+100,
		"delivery_item_bid": 'xx121212x'
	}
	msgutil.send_message(topic_name, 'test_receive', data)
