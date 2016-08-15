# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.email_notify import EmailNotify


class AEmailNotify(api_resource.ApiResource):
	app = 'mall'
	resource = 'email_notify'

	@param_required(['owner_id', 'status'])
	def get(args):
		email_notify = EmailNotify.get({'owner_id': args['owner_id'], 'status': args['status']})

		return email_notify.to_dict()

	@param_required(['owner_id', 'status'])
	def post(args):
		is_active = args.get('is_active', None)
		if is_active is not None:
			is_active = int(is_active)
			email_notify = EmailNotify.get({'owner_id': args['owner_id'], 'status': args['status']})
			if is_active == 1:
				email_notify.enable()
			else:
				email_notify.disable()
		else:
			EmailNotify.modify({'owner_id': args['owner_id'], 'status': args['owner_id'], 'emails': args['emails']})

		return {}
