# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from business.mall.notify.email_notification import EmailNotification

class NotificationRepository(business_model.Service):
	def get_email_notifications(self):
		models = mall_models.UserOrderNotifySettings.select().dj_where(user_id=self.corp.id)

		return [EmailNotification(model) for model in models]

	def get_email_notification_by_type(self, type):
		model = mall_models.UserOrderNotifySettings.select().dj_where(user_id=self.corp.id, status=type).get()

		return EmailNotification(model)

	def get_email_notification_by_id(self, id):
		model = mall_models.UserOrderNotifySettings.select().dj_where(user_id=self.corp.id, id=id).get()

		return EmailNotification(model)
