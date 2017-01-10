# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.station_message.user_has_message_repository import UserHasMessageRepository


class AUserHasMessage(api_resource.ApiResource):
	"""
	用户关联站内消息
	"""
	app = "message"
	resource = "user_has_message"

	@param_required(['corp_id:int', 'message_id:int', 'is_read:bool'])
	def post(args):
		user_has_message = UserHasMessageRepository().get_user_has_message(args['corp_id'], args['message_id'])
		is_read = args.get('is_read', True)
		user_has_message.update(is_read)
		return {}
