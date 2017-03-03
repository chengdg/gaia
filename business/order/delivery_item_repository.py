# -*- coding: utf-8 -*-
"""
出货单
"""
from eaglet.core import paginator
from eaglet.core import watchdog
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.order.delivery_item import DeliveryItem

from business.order.order import Order

from db.mall import models as mall_models


class DeliveryItemRepository(business_model.Model):
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
		return DeliveryItemRepository(corp)

	def get_delivery_item(self, id, fill_options=None):
		db_models = mall_models.Order.select().dj_where(id=id)
		delivery_items = DeliveryItem.from_models(
			{"models": db_models, 'fill_options': fill_options, 'corp': self.corp})

		if delivery_items:
			return delivery_items[0]
		else:
			return None


	def get_delivery_items(self, filters, page_info, fill_options=None):
		db_models = mall_models.Order.select().dj_where(supplier=self.corp.id, origin_order_id__gt=0)
		pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)
		delivery_items = DeliveryItem.from_models(
			{"models": db_models, 'fill_options': fill_options, 'corp': self.corp})

		return pageinfo, delivery_items


	def get_delivery_item_by_bid(self, bid, fill_options=None):
		db_models = mall_models.Order.select().dj_where(order_id=bid)

		delivery_items = DeliveryItem.from_models(
			{"models": db_models, 'fill_options': fill_options, 'corp': self.corp})

		if delivery_items:
			return delivery_items[0]
		else:
			return None

	def __get_db_models_for_corp(self):
		webapp_id = self.corp.webapp_id
		db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id, webapp_user_id__gt=0)

		return db_models

	def get_delivery_items_by_order_id(self, order_id):
		db_models = self.__get_db_models_for_corp()

		db_models = db_models.dj_where(origin_order_id=order_id)
		delivery_items = DeliveryItem.from_models(
			{"models": db_models, 'fill_options': {}, 'corp': self.corp})

		return delivery_items
