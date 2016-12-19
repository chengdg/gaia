# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business.station_message.message_repository import MessageRepository

class AMessages(api_resource.ApiResource):
    """
    商品分类集合
    """
    app = "message"
    resource = "messages"

    def get(args):
        # corp = args['corp']
        # messages = corp.message_repository.get_messages()
        msgrepo = MessageRepository()
        messages = msgrepo.get_messages()
        datas = []
        for message in messages:
            datas.append({
                'id': message.id,
                'title': message.title,
                'content': message.content,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M'),
            })

        return {
            'messages': datas
        }