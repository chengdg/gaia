# -*- coding: utf-8 -*-
"""@package business.station_message.message
站内消息
"""
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.station_message import models as message_models

from business.station_message.message_attachment import MessageAttachment
from business.station_message.message_attachment_repository import MessageAttachmentRepository

class Message(business_model.Model):
	__slots__ = (
		'id',
		'title',
		'content',
		'file_url',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def update(self, title, content, attachments):
		"""
		更新站内消息
		"""
		message_models.Message.update(title=title, content=content).dj_where(id=self.id).execute()

		if attachments:
			MessageAttachmentRepository().delete_message_attachments(self.id)
			for attachment in attachments:
				MessageAttachment.create(self.id, attachment.get('name'), attachment.get('type'), attachment.get('path'))

	@staticmethod
	@param_required(['title', 'content', '?attachments:list'])
	def create(args):
		"""
		创建站内消息
		"""
		corp = CorporationFactory.get()
		attachments = args.get('attachments')
		model = message_models.Message.create(
			owner=corp.id,
			title=args.get('title').strip(),
			content=args.get('content').strip(),
			file_url='multifile'
		)
		if model and attachments:
			for attachment in attachments:
				MessageAttachment.create(model, attachment.get('name'), attachment.get('type'), attachment.get('path'))
		return Message(model)
