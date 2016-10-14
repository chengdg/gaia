# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AEmailNotifications(api_resource.ApiResource):
	"""
	运营邮件通知列表
	"""
	app = 'mall'
	resource = 'email_notifications'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		email_notifications = corp.notification_repository.get_email_notifications()

		datas = []
		for notification in email_notifications:
			datas.append({
				'id': notification.id,
				'type': notification.type,
				'is_active': notification.is_active,
				'email_addresses': notification.email_addresses,
				'black_member_ids':notification.black_member_ids 
			})

		return {
			'email_notifications': datas
		}
