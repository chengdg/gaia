# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.account.models import User
from business import model as business_model
from db.mall import models as mall_models
from db.account import models as account_models
from db.station_message import models as message_models
from business.station_message.message_attachment_repository import MessageAttachmentRepository
from business.station_message.user_has_message import UserHasMessage


class UserHasMessageRepository(business_model.Service):
	def create_user_has_messages(self, message):
		created_list = []
		# User表
		for user in User.select().where(id > 1):
			created_list.append({
				'user': user,
				'message': message,
			})
		message_models.UserHasMessage.insert_many(created_list).execute()

	def get_user_has_message(self, user_id, message_id):
		model = message_models.UserHasMessage.select().dj_where(user=user_id, message=message_id).get()
		return UserHasMessage(model)

	def get_unread_count(self, user_id):
		count = message_models.UserHasMessage.select().dj_where(user=user_id).count()
		return count

