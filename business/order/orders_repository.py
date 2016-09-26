# -*- coding: utf-8 -*-
"""
订单本
"""

from eaglet.core import watchdog
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model

from business.order.order import Order
from db.mall import models as mall_models

order_types = ('all', 'to_be_paid', 'to_be_shipped')


class OrdersRepository(business_model.Model):
	__slots__ = (
		'corp',
		'type'
	)

	def __init__(self, corp, order_type):
		business_model.Model.__init__(self)
		self.corp = corp
		self.type = order_type

	@staticmethod
	@param_required(['corp'])
	def get(args):
		# order_type = args['type']


		# owner = Owner.from_id({'owner_id': owner_id})
		corp = args['corp']
		return OrdersRepository(corp)

	# if order_type in order_types:
	# 	return OrdersRepository(corp, order_type)
	# else:
	# 	raise RuntimeError('Error orders_book type..')

	def __search(self, webapp_id, filter_values):
		return mall_models.Order.select().dj_where(webapp_id=webapp_id)

	def get_orders(self, filter_values):
		webapp_id = self.corp.webapp_id
		# db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id)
		db_models = self.__search(webapp_id, filter_values)
		self.context['db_models'] = db_models

		# self.orders = [Order(db_model) for db_model in db_models]

		orders = Order.fill_orders({"db_models": db_models, 'fill_options': {
			'with_products': True,
			'with_refund_info': True,
			'with_group_buy_info': True,
			'with_member': True

		}})

		return orders