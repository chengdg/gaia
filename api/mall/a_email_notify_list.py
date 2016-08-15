# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.email_notify import EmailNotify


class AEmailNotifyList(api_resource.ApiResource):
	app = 'mall'
	resource = 'email_notify_list'

	@param_required(['owner_id'])
	def get(args):
		email_notify_list = EmailNotify.get_from_owner_id({'owner_id': args['owner_id']})
		email_notify_list = map(lambda x: x.to_dict(), email_notify_list)
		return {'email_notify_list': email_notify_list}
