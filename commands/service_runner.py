# -*- coding: utf-8 -*-
"""
基于MNS的创建service runner

启动之后，不断轮询队列

@author Victor
"""

import json
import logging

from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.command import BaseCommand
from mns.account import Account
from mns.subscription import *

import settings
from service import handler_register

WAIT_SECONDS = 10
SLEEP_SECONDS = 10

class Command(BaseCommand):
	help = "python manage.py service_runner"
	args = ''

	# topic-queue模型中的queue

	def handle(self, *args, **options):
		global _SERVICE_LIST

		# 准备访问MNS
		self.mns_account = Account(\
			settings.MNS_ENDPOINT, \
			settings.MNS_ACCESS_KEY_ID, \
			settings.MNS_ACCESS_KEY_SECRET, \
			settings.MNS_SECURITY_TOKEN)

		queue = self.mns_account.get_queue(settings.SUBSCRIBE_QUEUE_NAME)
		logging.info('queue: {}'.format(queue.get_attributes().queue_name))

		# TODO: 改成LongPoll更好
		while True:
			handler_func = None
			handle_success = False
			#读取消息
			try:
				recv_msg = queue.receive_message(WAIT_SECONDS)
				logging.info("Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id))

				# 处理消息(consume)
				data = json.loads(recv_msg.message_body)
				message_name = data['name']
				handler_func = handler_register.find_message_handler(message_name)
				if handler_func:
					try:
						response = handler_func(data['data'], recv_msg)
						logging.info("service response: {}".format(response))
						handle_success = True

						#只有正常才能删除消息，否则消息仍然在队列中
						try:
							queue.delete_message(recv_msg.receipt_handle)
							logging.debug("Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle)
						except MNSException,e:
							logging.debug("Delete Message Fail! Exception:%s\n" % e)
					except:
						logging.info(u"Service Exception: {}".format(unicode_full_stack()))
				else:
					queue.delete_message(recv_msg.receipt_handle)
					#TODO: 这里是否需要删除消息？
					logging.info(u"Error: no such service found : {}".format(message_name))

			except MNSExceptionBase as e:
				if e.type == "QueueNotExist":
					logging.debug("Queue not exist, please create queue before receive message.")
					break
				elif e.type == "MessageNotExist":
					logging.debug("Queue is empty! Waiting...")
				else:
					logging.debug("Receive Message Fail! Exception:%s\n" % e)
				time.sleep(SLEEP_SECONDS)
				continue
			except Exception as e:
				print u"Exception: {}".format(unicode_full_stack())
			finally:
				try:
					_data = data['data']
				except:
					_data = 'null'

				if handler_func:
					message = {
						'message_id': recv_msg.message_id,
						'message_body_md5': '',
						'data': _data,
						'topic_name': '',
						'msg_name': message_name,
						'handel_success': handle_success
					}
					watchdog.info(message, log_type='MNS_RECEIVE_LOG')
		return
