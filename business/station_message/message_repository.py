# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from db.account import models as account_models
from db.station_message import models as message_models
from business.station_message.message import Message


class MessageRepository(business_model.Service):
	def get_messages(self):
		models = message_models.Message.select()
		return [Message(model) for model in models]

	@param_required(['id'])
	def get_message(self, id):
		model = message_models.Message.select().dj_where(id=id).get()
		return Message(model)

	@param_required(['id'])
	def delete_message(self, id):
		"""
		删除指定的站内消息
		"""
		message_models.Message.delete().dj_where(id=id).execute()
