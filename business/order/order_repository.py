# -*- coding: utf-8 -*-
"""
订单
"""
from eaglet.core import paginator
from eaglet.core import watchdog

from business.common.page_info import PageInfo
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.common.filter_parser import FilterParser
from business.order.order import Order

from db.mall import models as mall_models


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

	def __search(self, filters):
		# db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id, origin_order_id__lte=0)

		should_in_order_ids = []
		db_models = self.__get_db_models_for_corp()

		order_ids = [db_model for db_model in db_models]

		ohs_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=order_ids)

		# 处理订单中的值搜索
		if filters:
			order_filter_parse_result = {}
			if '__f-ship_tel-equal' in filters:
				filter_parse_result = FilterParser.get().parse_key(filters, '__f-ship_tel-equal')
				order_filter_parse_result.update(filter_parse_result)
			if '__f-ship_name-equal' in filters:
				filter_parse_result = FilterParser.get().parse_key(filters, '_f-ship_name-equal')
				order_filter_parse_result.update(filter_parse_result)
			if '__f-order_bid-equal' in filters:
				filter_parse_result = FilterParser.get().parse_key(filters, '__f-order_bid-equal',
				                                                   {'order_bid': 'order_id'})
				order_filter_parse_result.update(filter_parse_result)
			if '__f-weizoom_card_money-gt' in filters:
				filter_parse_result = FilterParser.get().parse_key(filters, '__f-weizoom_card_money-gt')
				order_filter_parse_result.update(filter_parse_result)

			# if '__f-product_name-contain' in filters:
			# 	filter_parse_result = FilterParser.get().parse_key(filters, '__f-product_name-contain',
			# 	                                                   {'product_name': 'name'})
			# 	target_page = PageInfo.get_max_page()
			# 	products, pageinfo = self.corp.product_pool.get_products(filter_parse_result, target_page)
			# 	product_ids = [product.id for product in products]
			# 	ohs_list = ohs_list.dj_where(product_id__in=product_ids)
			#
			# 	_order_ids = [ohs.order_id for ohs in ohs_list]
			#
			# 	should_in_order_ids.append(_order_ids)

			# if should_in_order_ids:
			# 	order_filter_parse_result.update({
			# 		'id__in': should_in_order_ids
			# 	})

			if order_filter_parse_result:
				db_models = db_models.dj_where(**order_filter_parse_result)
			if should_in_order_ids:
				db_models = db_models.dj_where(id__in=should_in_order_ids)
		print('-----db_models-x', db_models)

		print(db_models)
		# print('-----db_models-count',db_models.count())
		return db_models

	def get_orders(self, filters, target_page, fill_options):

		# db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id)
		db_models = self.__search(filters)

		pageinfo, db_models = paginator.paginate(db_models, target_page.cur_page, target_page.count_per_page)

		self.context['db_models'] = db_models

		orders = Order.from_models({"db_models": db_models, 'fill_options': fill_options, 'corp': self.corp})

		return pageinfo, orders

	def get_order(self, id, fill_options=None):
		db_models = self.__get_db_models_for_corp()
		db_model = db_models.dj_where(id=id)
		orders = Order.from_models({"db_models": db_model, 'fill_options': fill_options, 'corp': self.corp})

		if orders:
			return orders[0]
		else:
			return None

	def __get_db_models_for_corp(self):
		webapp_id = self.corp.webapp_id
		user_id = self.corp.id
		sync_able_status_list = [mall_models.ORDER_STATUS_PAYED_SUCCESSED,
		                         mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
		                         mall_models.ORDER_STATUS_PAYED_SHIPED,
		                         mall_models.ORDER_STATUS_SUCCESSED]

		if self.corp.type != 'normal' and self.corp.type != 'multi_shop':
			db_models = mall_models.Order.select().dj_where(webapp_id=webapp_id, origin_order_id__lte=0,
			                                                webapp_user_id__gt=0)
		else:
			# 加载同步订单
			db_models = mall_models.Order.select().dj_where(webapp_user_id__gt=0).where(
				(mall_models.Order.webapp_id == webapp_id) | (
					(mall_models.Order.supplier_user_id == user_id) & (mall_models.Order.origin_order_id > 0) & (
						mall_models.Order.status << sync_able_status_list)))

		# 过滤团购订单，团购订单只显示团购成功和团购退款中、团购退款成功的订单
		group_order_relations = mall_models.OrderHasGroup.select().dj_where(webapp_id=webapp_id)

		if group_order_relations.count() > 0:
			# 团购成功的订单
			successful_group_order_bids = []

			# 团购失败的订单
			failed_group_order_bids = []
			# 进行中的团购
			running_group_order_bids = []

			for g in group_order_relations:
				if g.group_status == mall_models.GROUP_STATUS_OK:
					successful_group_order_bids.append(g.order_id)
				elif g.group_status == mall_models.GROUP_STATUS_failure:
					failed_group_order_bids.append(g.order_id)
				elif g.group_status == mall_models.GROUP_STATUS_ON:
					running_group_order_bids.append(g.order_id)
				else:
					pass

			# 忽略的团购订单
			ignored_group_orders = db_models.where(
				(mall_models.Order.order_id << running_group_order_bids) | (
					(mall_models.Order.order_id << failed_group_order_bids) & (mall_models.Order.status.not_in(
						[mall_models.ORDER_STATUS_GROUP_REFUNDING, mall_models.ORDER_STATUS_GROUP_REFUNDING]))))

			ignored_order_bids = [o.order_id for o in ignored_group_orders]

			db_models = db_models.dj_where(order_id__notin=ignored_order_bids)

		return db_models
