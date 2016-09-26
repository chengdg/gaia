# -*- coding: utf-8 -*-
"""
订单
"""

from eaglet.core import watchdog
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model

from business.order.order import Order
from db.mall import models as mall_models

order_types = ('all', 'to_be_paid', 'to_be_shipped')


class OrderRepository(business_model.Model):
	__slots__ = (
		'corp',
		'type'
	)

	def __init__(self, corp):
		business_model.Model.__init__(self)
		self.corp = corp

	@staticmethod
	@param_required(['corp'])
	def get(args):
		corp = args['corp']
		return OrderRepository(corp)


	def __search(self, webapp_id, filter_values):
		db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id, origin_order_id__lte=0)

		return db_models

	def get_orders(self, filter_values, target_page):
		webapp_id = self.corp.webapp_id
		# db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id)
		db_models = self.__search(webapp_id, filter_values)
		self.context['db_models'] = db_models

		# self.orders = [Order(db_model) for db_model in db_models]

		orders = Order.from_models({"db_models": db_models, 'fill_options': {

			'with_refund_info': True,
			'with_group_buy_info': True,
			'with_member': True,
			'with_delivery_items': {
				'fill': True,
				'fill_options': {
					'with_products': True
				}
			}

		}})

		return orders
