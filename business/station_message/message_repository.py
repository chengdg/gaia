# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from db.account import models as account_models
from db.station_message import models as message_models
from business.station_message.message import Message
from business.station_message.message_attachment_repository import MessageAttachmentRepository
from business.station_message.user_has_message_repository import UserHasMessageRepository


class MessageRepository(business_model.Service):
	def get_messages(self):
		models = message_models.Message.select().order_by(message_models.Message.created_at.desc())
		return [Message(model) for model in models]

	def get_message(self, id):
		model = message_models.Message.select().dj_where(id=id).get()

		return Message(model)

	# def get_message_attachments(self, id):
	# 	attachments = message_models.MessageAttachment.select().dj_where(message=id)
	# 	data = [{'id': at.id,
	# 					'name': at.file_name,
	# 					'type': at.file_type,
	# 					'path': at.path} for at in attachments]
	# 	return data

	def delete_message(self, id):
		"""
		删除指定的站内消息
		"""
		MessageAttachmentRepository().delete_message_attachments(id)
		UserHasMessageRepository().delete_user_has_message(id)
		message_models.Message.delete().dj_where(id=id).execute()
