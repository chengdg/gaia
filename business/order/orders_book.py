# -*- coding: utf-8 -*-
"""
订单本
"""

from eaglet.core import watchdog
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.owner import Owner
from business.order.order import Order
from db.mall import models as mall_models

order_types = ('all', 'to_be_paid', 'to_be_shipped')


class OrdersBook(business_model.Model):
	__slots__ = (
		'owner',
		'type',
		'orders'
	)

	def __init__(self, owner, order_type):
		business_model.Model.__init__(self)
		self.owner = owner
		self.type = order_type

	@staticmethod
	@param_required(['owner_id', 'type'])
	def get(args):

		order_type = args['type']
		owner_id = args['owner_id']

		owner = Owner.from_id({'owner_id': owner_id})

		if order_type in order_types:
			return OrdersBook(owner, order_type)
		else:
			raise RuntimeError('Error orders_book type..')

	def get_orders(self, filter_values):
		webapp_id = self.owner.webapp_id
		db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id)

		self.orders = [Order(db_model) for db_model in db_models]

		return self.orders


	@cached_context_property
	def count(self):
		return len(self.orders)

