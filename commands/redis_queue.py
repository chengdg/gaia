#!/usr/bin/python
# -*- coding: UTF-8 -*-

import redis
import settings
import json
import time

VisibilityTimeout = 10  # 取出消息隐藏时长

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_QUEUE_DB)


class Message(object):
	def __init__(self, message):
		self.message_body = message['message_body']
		self.message_id = message['message_id']
		self.receipt_handle = self
		self.queue_value = json.dumps(message)


class Queue(object):
	def __init__(self, queue_name):
		self.queue_name = queue_name

	def receive_message(self, WAIT_SECONDS):
		while True:
			_message = r.brpop(self.queue_name)[1]
			message = json.loads(_message)
			status = message.setdefault('status', 'waiting')
			if status == 'waiting':
				message['status'] = 'processing'
				message['processing_from'] = time.time()
				r.lpush(self.queue_name, json.dumps(message))

				return Message(message)
			elif status == 'processing':

				if message['processing_from'] + VisibilityTimeout < time.time():
					message['status'] = 'waiting'

				r.lpush(self.queue_name, json.dumps(message))

	def get_attributes(self):
		return self

	def delete_message(self, receipt_handle):
		r.lrem(self.queue_name, receipt_handle.queue_value)


def get_queue(name):
	return Queue(name)
