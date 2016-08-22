# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.email_notify import EmailNotification


class AEmailNotification(api_resource.ApiResource):
	"""
	运营邮件通知
	"""
	app = 'mall'
	resource = 'email_notification'

	@param_required(['owner_id', 'status'])
	def get(args):
		email_notify = EmailNotification.get({'owner_id': args['owner_id'], 'status': args['status']})

		return email_notify.to_dict()

	@param_required(['owner_id', 'status'])
	def post(args):
		is_active = args.get('is_active', None)
		if is_active is not None:
			is_active = int(is_active)
			email_notify = EmailNotification.get({'owner_id': args['owner_id'], 'status': args['status']})
			if is_active == 1:
				email_notify.enable()
			else:
				email_notify.disable()
		else:
			EmailNotification.modify({'owner_id': args['owner_id'], 'status': args['status'], 'emails': args['emails'],'member_ids':args['member_ids']})

		return {}

		if 1:
			return {}
		else:
			500,{'msg'}
