# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business.station_message.message_repository import MessageRepository
from business.station_message.user_has_message_repository import UserHasMessageRepository

class AMessages(api_resource.ApiResource):
    """
    商品分类集合
    """
    app = "message"
    resource = "messages"

    @param_required(['user_id:int'])
    def get(args):
        # corp = args['corp']
        # messages = corp.message_repository.get_messages()
        msgrepo = MessageRepository()
        uhm_repo = UserHasMessageRepository()

        messages = msgrepo.get_messages()
        datas = []
        for message in messages:
            is_read = uhm_repo.get_user_has_message(args['user_id'], message.id).is_read
            datas.append({
                'id': message.id,
                'title': message.title,
                'content': message.content,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_read': is_read
            })
        unread_count = uhm_repo.get_unread_count(args['user_id'])

        return {
            'messages': datas,
            'unread_count': unread_count
        }