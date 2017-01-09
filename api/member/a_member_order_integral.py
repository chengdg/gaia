# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.member.member_spread import MemberSpread


class AMemberOrderIntegral(api_resource.ApiResource):
	"""
	已支付的订单
	"""
	app = 'member'
	resource = 'member_order_integral'


	@param_required(['corp','order_id'])
	def post(args):

		order_id = args['order_id']
		corp = args['corp']
		# from_status = args['from_status']
		# to_status = args['to_status']
		fill_options = {
			'with_member': True,
			'with_delivery_items': {
				'with_products': True,
			}

		}
		order = corp.order_repository.get_order(order_id, fill_options)

		member = corp.member_repository.get_member_by_id(order.member_info['id'])

		member.increase_integral_after_finish_order(order)  # 对应购买商品返积分功能
		# member.update_pay_info(order, from_status, to_status)
		# MemberSpread.process_order_from_spread({'order_id': order.id})
