# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.email_notify import EmailNotification


class AEmailNotifications(api_resource.ApiResource):
	"""
	运营邮件通知列表
	"""
	app = 'mall'
	resource = 'email_notifications'

	@param_required(['owner_id'])
	def get(args):
		email_notifications = EmailNotification.get_from_owner_id({'owner_id': args['owner_id']})
		email_notifications = map(lambda x: x.to_dict(), email_notifications)
		return {'email_notifications': email_notifications}
