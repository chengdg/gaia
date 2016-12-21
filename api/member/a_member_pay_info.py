# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required



class AMemberPayInfo(api_resource.ApiResource):
	"""
	已支付的订单
	"""
	app = 'member'
	resource = 'member_pay_info'

	@param_required(['corp', 'order_id', 'from_status', 'to_status'])
	def post(args):
		order_id = args['order_id']
		corp = args['corp']
		from_status = args['from_status']
		to_status = args['to_status']
		fill_options = {
			'with_member': True,
			'with_delivery_items': {
				'with_products': True,
			}

		}
		order = corp.order_repository.get_order(order_id, fill_options)

		member = corp.member_repository.get_member_by_id(order.member_info['id'])

		member.update_pay_info(order, from_status, to_status)
