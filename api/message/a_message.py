# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.station_message.message import Message


class AMessage(api_resource.ApiResource):
    """
    商品分类
    """
    app = "message"
    resource = "message"

    @param_required(['corp_id', 'title', 'content', 'file_url'])
    def put(args):
        message = Message.create({
            'title': args['title'],
            'content': args['content'],
            'file_url': args['file_url']
        })
        return {
            'id': message.id
        }

    @param_required(['corp_id', 'id', 'title', 'content', 'file_url'])
    def post(args):
        corp = args['corp']
        name = args['name']
        classification_id = args['id']
        note = args.get('note', '')

        message = corp.message_repository.get_message(classification_id)
        message.update(name, note)

        return {}

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        classification_id = args['id']
        message = corp.message_repository.get_message(classification_id)
        if message.is_used_by_product():
            return 500, 'used_by_product' #商品分类正在被使用
        else:
            corp.message_repository.delete_message(classification_id)

            return {}
