# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.order.order_repository import OrderRepository


class AOrderList(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'order'
	resource = 'orders'

	# @param_required(['owner_id', 'cur_page', 'count_per_page', 'order_type'])
	@param_required(['cur_page', 'count_per_page'])
	def get(args):

		filter_values = args.get('filter_values', '')

		corp = args['corp']
		order_repository = corp.order_repository

		try:
			target_page = PageInfo.create({
				"cur_page": int(args.get('cur_page', 1)),
				"count_per_page": int(args.get('count_per_page', 10))
			})
			fill_options = {
				'with_refunding_info': True,
				'with_group_buy_info': True,
				'with_member': True,
				'with_group_info': True,
				'with_full_money_info': True,
				'with_delivery_items': {
					'fill': True,
					'fill_options': {
						'with_products': True,
						'with_refunding_info': True
					}
				}

			}
			orders = order_repository.get_orders(filter_values, target_page, fill_options)
		except BaseException as e:
			# todo 去掉
			from eaglet.core.exceptionutil import unicode_full_stack
			watchdog.alert({
				'traceback': unicode_full_stack(),
				'uuid': 'a_orders error',
				'corp_id': args['corp'].id
			})
			print(unicode_full_stack())

			# raise e

		order_dicts = [order.to_dict() for order in orders]
		return {
			'page_info': target_page.to_dict(),
			'orders': order_dicts
		}
