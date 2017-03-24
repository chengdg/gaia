# -*- coding: utf-8 -*-
"""
出货单
"""
import json

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

	def __get_db_models_for_corp(self):
		return mall_models.Order.select().dj_where(supplier=self.corp.id, origin_order_id__gt=0, status__gt=mall_models.ORDER_STATUS_CANCEL)

	def __search(self, filters):
		db_models = self.__get_db_models_for_corp()
		if filters:
			if '__f-bid-equal' in filters:
				db_models = db_models.dj_where(order_id=filters['__f-bid-equal'])
			if '__f-product_name-contain' in filters:
				order_relations = mall_models.OrderHasProduct.select().dj_where(
					product_name__icontains=filters['__f-product_name-contain'])
				ids = [o.order_id for o in order_relations]
				db_models = db_models.dj_where(id__in=ids)
			if '__f-status-in' in filters:
				status = mall_models.MEANINGFUL_WORD2ORDER_STATUS[json.loads(filters['__f-status-in'])[0]]
				status_params = []

				if status == mall_models.ORDER_STATUS_REFUNDING:
					status_list = [mall_models.ORDER_STATUS_REFUNDING, mall_models.ORDER_STATUS_GROUP_REFUNDING]
				elif status == mall_models.ORDER_STATUS_REFUNDED:
					status_list = [mall_models.ORDER_STATUS_REFUNDED, mall_models.ORDER_STATUS_GROUP_REFUNDED]
				else:
					status_list = [status]
				status_params.extend(status_list)

				db_models = db_models.dj_where(status__in=status_params)
			if '__f-created_at-range' in filters:
				filters['__f-created_at-range'] = json.loads(filters['__f-created_at-range'])
				db_models = db_models.dj_where(created_at__range=filters['__f-created_at-range'])

		#倒序
		db_models = db_models.order_by(mall_models.Order.id.desc())

		return db_models

	def get_delivery_items(self, filters, page_info, fill_options=None):
		db_models = self.__search(filters)
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

	def get_delivery_items_by_order_id(self, order_id):
		db_models = mall_models.Order.select().dj_where(origin_order_id=order_id)
		delivery_items = DeliveryItem.from_models(
			{"models": db_models, 'fill_options': {}, 'corp': self.corp})

		return delivery_items
