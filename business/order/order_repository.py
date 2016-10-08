# -*- coding: utf-8 -*-
"""
订单
"""
from eaglet.core import paginator
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

	def get_orders(self, filter_values, target_page, fill_options):
		webapp_id = self.corp.webapp_id
		# db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id)
		db_models = self.__search(webapp_id, filter_values)

		pageinfo, db_models = paginator.paginate(db_models, target_page.cur_page, target_page.count_per_page)

		self.context['db_models'] = db_models

		# self.orders = [Order(db_model) for db_model in db_models]

		orders = Order.from_models({"db_models": db_models, 'fill_options': fill_options})

		return pageinfo, orders

	def get_order(self, id, fill_options):
		webapp_id = self.corp.webapp_id
		db_model = mall_models.Order.get(webapp_id=webapp_id, id=id)

		order = Order.from_models({"db_models": [db_model], 'fill_options': fill_options})[0]

		return order
