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
from business.order.order_repository import OrderRepository


class AOrderList(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'order'
	resource = 'orders'

	# @param_required(['owner_id', 'cur_page', 'count_per_page', 'order_type'])
	@param_required(['owner_id', 'cur_page', 'count_per_page'])
	def get(args):
		owner_id = args['owner_id']
		# order_type = args['order_type']

		filter_values = args.get('filter_values','')

		orders_repository = OrderRepository.get({'corp': args['corp']})

		try:
			orders = orders_repository.get_orders(filter_values)
		except:
			from eaglet.core.exceptionutil import unicode_full_stack
			print(unicode_full_stack())

		order_dicts = [order.to_dict() for order in orders]
		print('-------order_dicts',order_dicts)
		return {
			'page_info': '',
			'orders': order_dicts
		}
