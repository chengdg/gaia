# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AEmailNotification(api_resource.ApiResource):
	"""
	运营邮件通知
	"""
	app = 'mall'
	resource = 'email_notification'

	@param_required(['corp_id', 'id'])
	def get(args):
		corp = args['corp']
		notification = corp.notification_repository.get_email_notification_by_id(args['id'])

		return {
			'id': notification.id,
			'type': notification.type,
			'is_active': notification.is_active,
			'email_addresses': notification.email_addresses,
			'black_member_ids':notification.black_member_ids 
		}

	@param_required(['corp_id', 'id', 'email_addresses', 'black_member_ids'])
	def post(args):
		corp = args['corp']
		notification = corp.notification_repository.get_email_notification_by_id(args['id'])

		email_addresses = json.loads(args['email_addresses'])
		black_member_ids = json.loads(args['black_member_ids'])
		notification.update(email_addresses, black_member_ids)
		
		return {}