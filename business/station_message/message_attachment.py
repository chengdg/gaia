# -*- coding: utf-8 -*-
"""@package business.station_message.message
站内消息
"""
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.station_message import models as message_models


class MessageAttachment(business_model.Model):
	__slots__ = (
		'id',
		'message'
		'filename',
		'type',
		'path',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)


	def update(self, title, content, file_url):
		"""
		更新站内消息
		"""
		message_models.Message.update(title=title, content=content, file_url=file_url).dj_where(id=self.id).execute()

	@staticmethod
	def create(message, filename, type_name, path):
		"""
		创建消息的附件
		"""
		model = message_models.MessageAttachment.create(
			message=message,
			filename=filename,
			type=type_name,
			path=path
		)
		return MessageAttachment(model)

	def delete(self, message_id):
		"""
		删除与message相关的docments
		"""
		message_models.MessageAttachment.delete().dj_where(message=message_id).execute()
