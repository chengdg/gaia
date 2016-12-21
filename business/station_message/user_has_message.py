# -*- coding: utf-8 -*-
"""@package business.station_message.user_has_message
用户关联站内消息
"""

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.station_message import models as message_models
from db.account.models import User

from business.station_message.message_attachment import MessageAttachment
from business.station_message.message_attachment_repository import MessageAttachmentRepository


class UserHasMessage(business_model.Model):
	__slots__ = (
		'id',
		'user',
		'message',
		'is_read',
		'message_type'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def update(self, is_read):
		message_models.UserHasMessage.update(is_read=is_read).dj_where(id=self.id).execute()
