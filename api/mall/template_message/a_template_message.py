# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

class ATemplateMessage(api_resource.ApiResource):
	"""
	模板消息
	"""
	app = 'mall'
	resource = 'template_message'

	@param_required(['corp', 'send_point'])
	def get(args):
		corp = args['corp']
		send_point = args['send_point']
		template_message_detail, template_message = corp.template_message_detail_repository.get_template_message(corp.id, send_point)
		template_message_detail.attribute = template_message.attribute
		template_message_detail.title = template_message.title
		template_dic = {
			'title':template_message_detail.title,
			'template_id':template_message_detail.template_id,
			'attribute':template_message_detail.attribute,
			'first_text':template_message_detail.first_text,
			'remark_text':template_message_detail.remark_text
		}
		return {
            'template': template_dic
        }