# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AEmailNotificationActivity(api_resource.ApiResource):
	"""
	运营邮件通知的开启状态
	"""
	app = 'mall'
	resource = 'email_notification_activity'

	@param_required(['corp_id', 'id', 'activity'])
	def post(args):
		corp = args['corp']
		notification = corp.notification_repository.get_email_notification_by_id(args['id'])

		activity = args['activity']
		if 'on' == activity:
			notification.enable()
		elif 'off' == activity:
			notification.disable()
		else:
			pass

		return {}