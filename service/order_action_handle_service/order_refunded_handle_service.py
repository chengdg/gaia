# -*- coding: utf-8 -*-
"""


@author Victor
"""

from bdem import msgutil

from business.mall.corporation import Corporation
from business.order.release_order_resource_service import ReleaseOrderResourceService
from service.service_register import register
from gaia_conf import TOPIC


@register("order_cancelled")
def process(data, recv_msg=None):
	corp_id = data['corp_id']
	order_id = data['order_id']
	order_bid = data['order_bid']
	corp = Corporation(corp_id)
	from_status = data['from_status']
	to_status = data['to_status']

	# 释放订单资源
	release_order_resource_service = ReleaseOrderResourceService.get(corp)
	release_order_resource_service.release(order_id, from_status, to_status)

	# 更新会员信息

	# 发送运营邮件通知
	topic_name = TOPIC['base_service']
	data = {
		"type": "order",
		"order_id": order_id,
		"corp_id": corp.id
	}
	msgutil.send_message(topic_name, 'send_order_email_task', data)

	# 发送模板消息
	topic_name = TOPIC['base_service']
	data = {
		"order_id": order_id,
		"corp_id": corp.id
	}
	msgutil.send_message(topic_name, 'send_order_template_message_task', data)

	fill_options = {
		'with_member': True
	}
	order = corp.order_repository.get_order(order_id, fill_options)
	member = corp.member_repository.get_member_by_id(order.member_info['id'])
	member.update_pay_info(order, from_status, to_status)
