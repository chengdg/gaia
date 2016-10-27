# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class AOrderList(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'order'
	resource = 'orders'

	@param_required(['corp'])
	def get(args):
		filters = json.loads(args.get('filters', '{}'))

		corp = args['corp']
		order_repository = corp.order_repository

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
				'with_products': True,
				'with_refunding_info': True,
				'with_express_details': True,
				'with_supplier': True
			}

		}
		pageinfo, orders = order_repository.get_orders(filters, target_page, fill_options)

		# todo 手工展开
		order_dicts = [order.to_dict() for order in orders]
		return {
			'page_info': pageinfo.to_dict(),
			'orders': order_dicts
		}
