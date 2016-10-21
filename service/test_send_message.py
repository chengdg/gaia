#coding: utf8
from bdem import msgutil

topic_name = 'new-zeus-test'
msg_name = 'test_order_paid'
data = {
	"order_id": 32,
	"corp_id": 43,
	"from_status": "created",
	"to_status": "paid",
	"tettt":111111111
}
msgutil.send_message(topic_name, msg_name, data)