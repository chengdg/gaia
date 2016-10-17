from bdem import msgutil



topic_name = 'test-topic'
data = {
	"delivery_item_id": 999999,
	"delivery_item_bid": 'xx121212x'
}
msgutil.send_message(topic_name, 'demo_data111', data)



