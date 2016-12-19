# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from db.account import models as account_models
from db.station_message import models as message_models


class MessageAttachmentRepository(business_model.Service):
	def get_message_attachments(self, id):
		attachments = message_models.MessageAttachment.select().dj_where(message=id)
		data = [{'id': at.id,
						'name': at.filename,
						'type': at.type,
						'path': at.path} for at in attachments]
		return data

	def delete_message_attachments(self, message_id):
		"""
		删除指定的站内消息的附件
		"""
		message_models.MessageAttachment.delete().dj_where(message=message_id).execute()
