# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.summary_operation import SummaryOperation

class AShopRemind(api_resource.ApiResource):
	'''
	经营概况集合.
	'''
	app = 'mall'
	resource = 'summary_operation'

	@param_required(['owner_id'])
	def get(args):
		'''
		经营概况
		'''
		summary_operation = SummaryOperation.from_owner_id({
				'owner_id': args['owner_id'],
				'with_options': {
					'with_unread_message_count': True,   # 未读消息
					'with_new_member_count': True,  # 昨日新增会员
					'with_order_count': True,   #  昨日下单数
					'with_order_money': True,   # 昨日成交额
					'with_subscribed_member_count': True   # 关注会员
				}
			})
		return {
			'summary_operation': summary_operation.to_dict()
		}
