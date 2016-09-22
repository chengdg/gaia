# -*- coding: utf-8 -*-
import json
from datetime import datetime

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.account.user_profile import UserProfile
from business.mall.order_has_group import OrderHasGroup
from business.order.orders_repository import OrdersRepository


class AOrderList(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'order'
	resource = 'orders2'

	# @param_required(['owner_id', 'cur_page', 'count_per_page', 'order_type'])
	@param_required(['owner_id', 'cur_page', 'count_per_page', 'order_type'])
	def get(args):
		owner_id = args['owner_id']
		# order_type = args['order_type']

		filter_values = args['filter_values']

		orders_book = OrdersRepository.get({'owner_id': owner_id})

		orders = orders_book.get_orders(filter_values)

		order_dicts = [order.to_dict() for order in orders]

		return {
			'page_info': '',
			'orders': order_dicts
		}
