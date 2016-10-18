# -*- coding: utf-8 -*-

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
		相对于订单列表的增量信息：状态日志、操作日志、物流信息、完整的促销信息、优惠券信息
		@return:
		"""

		# todo 操作日志
		id = args['id']

		corp = args['corp']
		order_repository = corp.order_repository
		fill_options = {
			'with_refunding_info': True,
			'with_group_buy_info': True,
			'with_member': True,
			'with_group_info': True,
			'with_full_money_info': True,
			'with_status_logs': True,
			'with_operation_logs': True,
			'with_delivery_items': {
				'with_products': True,
				'with_refunding_info': True,
				'with_express_details': True,
				'with_supplier': True,
				'with_operation_logs': True
			}

		}

		order = order_repository.get_order(id, fill_options)
		# todo 显式声明
		if order:
			return {'order': order.to_dict()}
		else:
			return 500, {}

	@param_required(['id'])
	def post(args):
		"""
		修改订单信息，目前会修改的只有价格
		@return:
		"""
		corp = args['corp']
		id = args['id']

		order_repository = corp.order_repository
		order = order_repository.get_order(id)
		if order:

			if 'new_final_price' in args:
				new_final_price = float(args['new_final_price'])

				is_success, msg = order.update_final_price(corp, new_final_price)

			if 'new_remark' in args:
				remark = args['new_remark'].strip()
				is_success, msg = order.update_remark(corp, remark)

			else:
				is_success = False
				msg = 'error args'

			if is_success:
				return {}
			else:
				return 500, {'msg': msg}
		else:
			return 500, {}
