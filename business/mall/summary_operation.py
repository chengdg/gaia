# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from core import paginator
from core import dateutil

from db.mall import models as mall_models
from db.member import models as member_models
from db.mall import promotion_models 
from business.mall.product import Product
from business.account.user_profile import UserProfile
class SummaryOperation(business_model.Model):
	"""
	经营概况集合
	此类 主要是首页经营概况功能
	"""
	__slots__ = (
		'unread_message_count',  # 未读消息
		'new_member_count',  # 昨日新增会员
		'order_count',  #  昨日下单数
		'order_money',  # 昨日成交额
		'subscribed_member_count',  # 关注会员
	)
	
	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['owner_id', 'with_options'])
	def from_owner_id(args):
		summary_operation = SummaryOperation()
		user_profile = UserProfile.from_user_id({'user_id': args['owner_id']})
		options = args['with_options']
		SummaryOperation.__with_options(user_profile, summary_operation, options)
		return summary_operation

	@staticmethod
	def __with_options(user_profile, summary_operation, options):
		
		webapp_id = user_profile.webapp_id
		if options.get('with_unread_message_count', None):
			summary_operation.__unread_message_count(webapp_id)

		if options.get('with_new_member_count', None):
			summary_operation.__new_member_count(webapp_id)

		if options.get('with_order_count', None):
			summary_operation.__order_count(webapp_id)

		if options.get('with_order_money', None):
			summary_operation.__order_money(webapp_id)

		if options.get('with_subscribed_member_count', None):
			summary_operation.__subscribed_member_count(webapp_id)

	def __unread_message_count(self, webapp_id):
		#TODO 获取未读的微信信息
		self.unread_message_count = 0

	def __new_member_count(self, webapp_id):
		# 获得昨日订单数据
		today = '%s 23:59:59' % dateutil.get_yesterday_str('today')
		yesterday = '%s 00:00:00' % dateutil.get_yesterday_str('today')
		new_member_count = member_models.Member.select().dj_where(
			webapp_id=webapp_id, 
			created_at__gte=yesterday, 
			created_at__lte=today, 
			status=member_models.SUBSCRIBED, 
			is_for_test=False
		).count()
		self.new_member_count = new_member_count

	def __order_count(self, webapp_id):
		# orders = self.belong_to(webapp_id)
		# print orders
		#TODO 获取昨天交易订单
		self.order_count = 0

	def __order_money(self, webapp_id):
		#TODO 获取昨天订单交易额
		self.order_money = 0

	def __subscribed_member_count(self, webapp_id):
		subscribed_member_count = member_models.Member.select().dj_where(
			webapp_id=webapp_id, 
			is_subscribed=True, 
			is_for_test=False
		).count()
		self.subscribed_member_count = subscribed_member_count



	# def belong_to(self, webapp_id):
	# 	sync_able_status_list = [mall_models.ORDER_STATUS_PAYED_SUCCESSED,
	# 							 mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
	# 							 mall_models.ORDER_STATUS_PAYED_SHIPED,
	# 							 mall_models.ORDER_STATUS_SUCCESSED]

	# 	profile = UserProfile.from_webapp_id({'webapp_id': webapp_id})
	# 	user_id = profile.user_id
	# 	webapp_type = profile.webapp_type  # 1 自营，0是商户，2商品池， 3是多门店
	# 	if webapp_type:
	# 		orders = mall_models.Order.select().dj_where(webapp_id=webapp_id, origin_order_id__lte=0)
	# 	else:
	# 		# orders = mall_models.Order.filter(
	# 		# 	Q(webapp_id=webapp_id, origin_order_id__in=[-1,0]) | Q(supplier_user_id=user_id, origin_order_id__gt=0, status__in=sync_able_status_list)
	# 		# 	)
	# 		# print orders

	# 		orders = mall_models.Order.select().dj_where(webapp_id=webapp_id, origin_order_id__in=[-1,0])
	# 		orders_1 = mall_models.Order.select().dj_where(supplier_user_id=user_id, origin_order_id__gt=0, status__in=sync_able_status_list)
	# 		orders = (orders | orders_1)

	# 	group_order_relations = mall_models.OrderHasGroup.select().dj_where(webapp_id=webapp_id)
	# 	if group_order_relations.count() > 0:
	# 		group_order_ids = [r.order_id for r in group_order_relations]
	# 		not_pay_group_order_ids = [order.order_id for order in mall_models.Order.select().dj_where(
	# 			order_id__in=group_order_ids,
	# 			status=ORDER_STATUS_NOT
	# 			)
	# 		]
	# 		not_ship_group_on_order_ids = [order.order_id for order in mall_models.Order.select().dj_where(
	# 			order_id__in=[
	# 				r.order_id for r in group_order_relations.dj_where(
	# 				group_status__in=[GROUP_STATUS_ON, GROUP_STATUS_failure])
	# 				],
	# 				status=ORDER_STATUS_PAYED_NOT_SHIP
	# 			)]
	# 		cancel_group_order_ids = [order.order_id for order in mall_models.Order.select().dj_where(
	# 			order_id__in=[
	# 				r.order_id for r in group_order_relations.dj_where(
	# 				group_status__in=[GROUP_STATUS_OK, GROUP_STATUS_failure])
	# 				],
	# 				status=ORDER_STATUS_CANCEL,
	# 				pay_interface_type=PAY_INTERFACE_WEIXIN_PAY
	# 			)]
	# 		orders = orders.exclude(order_id__in=not_pay_group_order_ids+not_ship_group_on_order_ids+cancel_group_order_ids)
	# 	if not webapp_type:
	# 		sync_order_order_ids = [order.order_id for order in orders.dj_where(supplier_user_id=user_id)]
	# 		group_order_not_success_order_ids = [relation.order_id for relation in mall_models.OrderHasGroup.select().dj_where(
	# 								order_id__in=sync_order_order_ids,
	# 								group_status__in=[GROUP_STATUS_ON, GROUP_STATUS_failure])
	# 							]
	# 		orders = orders.dj_where(order_id__in=group_order_not_success_order_ids)
	# 	return orders



