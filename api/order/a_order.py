# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AOrder(api_resource.ApiResource):
	"""
	订单
	"""
	app = 'order'
	resource = 'order'

	@param_required(['id'])
	def get(args):
		"""
		特殊信息:相对于订单列表，状态日志、操作日志、物流信息
		@return:
		"""
		id = args['id']

		corp = args['corp']
		order_repository = corp.order_repository
		fill_options = {
			'with_refunding_info': True,
			'with_group_buy_info': True,
			'with_member': True,
			'with_group_info': True,
			'with_full_money_info': True,
			'status_logs': True,
			'with_delivery_items': {
				'fill': True,
				'fill_options': {
					'with_products': True,
					'with_refunding_info': True,
					'with_express_details': True
				}
			}

		}

		order = order_repository.get_order(id, fill_options)

		return {'order': order.to_dict()}
