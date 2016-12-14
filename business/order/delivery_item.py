# -*- coding: utf-8 -*-
"""
出货单
"""
from bdem import msgutil
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.supplier.supplier import Supplier
from business.mall.supplier.user_supplier import UserSupplier
from business.order.delivery_item_product_repository import DeliveryItemProductRepository
from business.order.process_order_after_delivery_item_service import ProcessOrderAfterDeliveryItemService
from db.express import models as express_models
from db.mall import models as mall_models
from util.send_phone_msg import send_phone_captcha
from gaia_conf import TOPIC
import logging


class DeliveryItem(business_model.Model):
	__slots__ = (
		'id',
		'bid',
		'origin_order_id',
		'webapp_id',
		'webapp_user_id',

		'postage',
		'status',
		'status_code',
		'express_company_name_value',
		'express_number',
		'leader_name',
		'created_at',
		'payment_time',
		'area',
		'ship_name',
		'supplier_id',
		'ship_address',

		'customer_message',

		'refunding_info',
		'supplier_info',
		'express_details',
		'has_db_record',  # 出货单使用出货单db，即db层面有出货单
		'with_logistics_trace',  # 是否使用快递100，对应于数据库里的is_100
		'with_logistics',  # 是否使用物流
		'operation_logs',
		'products'

	)

	@cached_context_property
	def express_company_name_text(self):
		express_company_name = self.context['corp'].express_delivery_repository.get_company_by_value(self.express_company_name_value)
		return express_company_name

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.id = db_model.id
		self.bid = db_model.order_id

		if db_model.origin_order_id > 0:
			self.origin_order_id = db_model.origin_order_id
		else:
			self.origin_order_id = db_model.id

		self.has_db_record = db_model.origin_order_id > 0  # 出货单使用出货单db，即db层面有出货单

		self.postage = db_model.postage
		self.webapp_id = db_model.webapp_id
		self.webapp_user_id = db_model.webapp_user_id

		self.status = db_model.status
		self.status_code = mall_models.ORDER_STATUS2MEANINGFUL_WORD[self.status]

		self.payment_time = db_model.payment_time
		self.area = db_model.area
		self.supplier_id = db_model.supplier
		self.ship_name = db_model.ship_name
		self.ship_address = db_model.ship_address
		self.customer_message = db_model.customer_message

		# 快递公司信息
		self.express_company_name_value = db_model.express_company_name
		self.express_number = db_model.express_number
		self.leader_name = db_model.leader_name
		self.created_at = db_model.created_at
		self.with_logistics_trace = db_model.is_100
		self.with_logistics = bool(db_model.express_company_name)
		self.context['db_model'] = db_model

	@cached_context_property
	def product_statistics_info(self):
		if not self.products:
			raise RuntimeError("You should fill products!")
		total_sale_price = 0
		product_names = []
		total_count = 0

		for product in self.products:
			total_sale_price += product.sale_price * product.count
			product_names.append(product.name)
			total_count += product.count
		return {
			'total_sale_price':total_sale_price,
			'product_names':product_names,
			'total_count':total_count
		}

	@staticmethod
	@param_required(['models'])
	def from_models(args):
		db_models = args['models']
		fill_options = args['fill_options']
		corp = args['corp']

		delivery_items = []
		delivery_item_ids = []

		for db_model in db_models:
			delivery_item = DeliveryItem(db_model)
			delivery_item.context['db_model'] = db_model
			delivery_item.context['corp'] = corp
			delivery_items.append(delivery_item)
			delivery_item_ids.append(delivery_item.id)

		if fill_options and delivery_items:
			if fill_options.get('with_products'):
				DeliveryItem.__fill_products(delivery_items)

			if fill_options.get('with_refunding_info'):
				DeliveryItem.__fill_refunding_info(delivery_items, delivery_item_ids)

			if fill_options.get('with_express_details'):
				DeliveryItem.__fill_express_details(delivery_items, delivery_item_ids)

			if fill_options.get('with_supplier'):
				DeliveryItem.__fill_supplier(delivery_items, delivery_item_ids)

			if fill_options.get('with_operation_logs'):
				DeliveryItem.__fill_operation_logs(delivery_items, delivery_item_ids)

		return delivery_items

	# suppliers = Supplier.from_ids()

	@staticmethod
	def __fill_express_details(delivery_items, delivery_item_ids):
		"""
		物流信息
		@param delivery_items:
		@param delivery_item_ids:
		@return:
		"""
		details = express_models.ExpressDetail.select().dj_where(order_id__in=delivery_item_ids).order_by(
			'-display_index')
		other_delivery_items = []
		if details.count() > 0:
			# 兼容历史数据,老数据里订单的发货信息直接关联到ExpressDetail
			delivery_item_id2details = {}

			for detail in details:
				if detail.order_id in delivery_item_id2details:
					delivery_item_id2details[detail.order_id].append(detail)
				else:
					delivery_item_id2details[detail.order_id] = [detail]

			for delivery_item in delivery_items:
				express_details = delivery_item_id2details.get(delivery_item.id)
				if express_details:
					for detail in express_details:
						delivery_item.express_details.append({
							'ftime': detail.ftime,
							'context': detail.context
						})
				else:

					other_delivery_items.append(delivery_items)
		else:
			other_delivery_items = delivery_items
		if other_delivery_items:
			express_company_name_values = []
			express_numbers = []
			for delivery_item in delivery_items:
				express_company_name_values.append(delivery_item.express_company_name_value)
				express_numbers.append(delivery_item.express_number)

				delivery_item.express_details = []

			express_push_list = express_models.ExpressHasOrderPushStatus.select().dj_where(
				express_company_name__in=express_company_name_values,
				express_number__in=express_numbers
			)

			name_number2express_push_id = {str(push.express_company_name + '__' + push.express_number): push.id for push
			                               in express_push_list}

			express_push_ids = []
			for push in express_push_list:
				express_push_ids.append(push.id)

			express_details = express_models.ExpressDetail.select().dj_where(express_id__in=express_push_ids)
			# express_push_id2details = {detail.express_id: detail for detail in express_details}
			express_push_id2details = {}
			for detail in express_details:
				if detail.express_id in express_push_id2details:
					express_push_id2details[detail.express_id].append(detail)
				else:
					express_push_id2details[detail.express_id] = [detail]

			for delivery_item in delivery_items:
				push_id = name_number2express_push_id.get(
					delivery_item.express_company_name_value + '__' + delivery_item.express_number)
				if push_id:
					express_details = express_push_id2details.get(push_id, [])

					for detail in express_details:
						delivery_item.express_details.append({
							'ftime': detail.ftime,
							'context': detail.context
						})

	@staticmethod
	def __fill_products(delivery_items):

		if delivery_items:
			corp = delivery_items[0].context['corp']
		else:
			corp = None
		delivery_item_product_repository = DeliveryItemProductRepository.get({'corp': corp})

		delivery_item_product_repository.set_products_for_delivery_items(delivery_items)

	# delivery_items_products = delivery_item_product_repository.get_products_for_delivery_items(
	# 	delivery_items=delivery_items,
	# 	with_premium_sale=True)
	#
	# delivery_item_id2products = {}
	# for product in delivery_items_products:
	# 	if product.delivery_item_id in delivery_item_id2products:
	# 		delivery_item_id2products[product.delivery_item_id].append(product)
	# 	else:
	# 		delivery_item_id2products[product.delivery_item_id] = [product]
	#
	# for delivery_item in delivery_items:
	# 	delivery_item.products = delivery_item_id2products[delivery_item.id]


	@staticmethod
	def __fill_operation_logs(delivery_items, delivery_item_ids):
		bids = [item.bid for item in delivery_items]

		logs = mall_models.OrderOperationLog.select().dj_where(order_id__in=bids)

		bid2logs = {}

		for log in logs:
			if log.order_id in bid2logs:
				bid2logs[log.order_id].append({
					'action_text': log.action,
					'time': log.created_at,
					'operator': log.operator
				})
			else:
				bid2logs[log.order_id] = [{
					'action_text': log.action,
					'time': log.created_at,
					'operator': log.operator
				}]

		for item in delivery_items:
			item.operation_logs = bid2logs.get(item.bid, [])
		# for log in item.operation_logs:
		# 	log['operator'] = item.leader_name

	def to_dict(self, *extras):

		result = business_model.Model.to_dict(self, *extras)
		if self.products:
			result['products'] = [product.to_dict() for product in self.products]

		return result

	@staticmethod
	def __fill_refunding_info(delivery_items, delivery_item_ids):
		refund_info_list = mall_models.OrderHasRefund.select().dj_where(delivery_item_id__in=delivery_item_ids)

		delivery_item_id2refund_info = {refund_info.delivery_item_id: refund_info for refund_info in refund_info_list}

		for delivery_item in delivery_items:
			total_product_sale_price = 0
			for product in delivery_item.products:
				total_product_sale_price += product.sale_price * product.count
			refunding_info = delivery_item_id2refund_info.get(delivery_item.id)
			if refunding_info:
				delivery_item.refunding_info = {
					'cash': refunding_info.cash,
					'weizoom_card_money': refunding_info.weizoom_card_money,
					'integral': refunding_info.integral,
					'integral_money': refunding_info.integral_money,
					'coupon_money': refunding_info.coupon_money,
					'total': refunding_info.total,
					'finished': refunding_info.finished,
					'total_can_refund': round(total_product_sale_price + delivery_item.postage, 2)
				}
			else:
				delivery_item.refunding_info = {
					'cash': 0,
					'weizoom_card_money': 0,
					'integral': 0,
					'integral_money': 0,
					'coupon_money': 0,
					'total': 0,
					'finished': False,
					'total_can_refund': round(total_product_sale_price + delivery_item.postage, 2)
				}

	@staticmethod
	def __fill_supplier(delivery_items, delivery_item_ids):

		# supplier_ids = [delivery_item.context['db_model'].supplier for delivery_item in delivery_items if
		#                 delivery_item.context['db_model'].supplier]

		supplier_ids = []
		supplier_user_ids = []
		for delivery_item in delivery_items:
			if delivery_item.context['db_model'].supplier:
				supplier_ids.append(delivery_item.context['db_model'].supplier)

			elif delivery_item.context['db_model'].supplier_user_id:
				supplier_user_ids.append(delivery_item.context['db_model'].supplier_user_id)

		corp = delivery_items[0].context['corp']

		# supplier
		suppliers = corp.supplier_repository.get_suppliers_by_ids(supplier_ids)
		id2supplier = {supplier.id: supplier for supplier in suppliers}

		# supplier

		supplier_users = UserSupplier.get_user_supplier_by_user_ids(supplier_user_ids)
		id2supplier_user = {supplier_user.id: supplier_user for supplier_user in supplier_users}

		for delivery_item in delivery_items:
			db_model = delivery_item.context['db_model']
			supplier_user = id2supplier_user.get(db_model.supplier_user_id, None)

			supplier = id2supplier.get(db_model.supplier, None)
			if supplier_user:
				delivery_item.supplier_info = {
					'name': supplier_user.name,
					'supplier_type': 'supplier_user',
					'supplier_tel':''
				}
			elif supplier:
				supplier = id2supplier.get(db_model.supplier, None)
				delivery_item.supplier_info = {
					'name': supplier.name,
					'supplier_type': 'supplier',
					'supplier_tel':supplier.supplier_tel
				}
			else:
				delivery_item.supplier_info = {
					'name': '',
					'supplier_type': 'None',
					'supplier_tel':''
				}

	def pay(self, payment_time, corp):
		"""
		支付出货单，只由pay_order触发
		@return:
		"""
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_PAYED_NOT_SHIP
		if self.has_db_record:
			action_text = u"支付"

			self.payment_time = payment_time
			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('delivery_item_paid', from_status, to_status)

	def cancel(self, corp):
		"""
		取消出货单，只有cancel_order触发
		@param corp:
		@return:
		"""
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_CANCEL
		if self.has_db_record:
			action_text = u"支付"

			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('delivery_item_cancelled', from_status, to_status)

	def finish(self, corp):
		"""
		完成出货单，可外部调用

		影响:
		- 更新订单状态
		- 记录状态日志
		- 记录操作日志


		- 更新红包引入消费金额的数据
		- 更新会员信息
		- 发送运营邮件通知
		- 发送短信通知
		- 更新红包引入消费金额的数据
		@param corp:
		@return:
		"""
		if self.status != mall_models.ORDER_STATUS_PAYED_SHIPED:
			return False, 'Error Status'
		action_text = u'完成'
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_SUCCESSED

		self.status = to_status

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)
		self.__save()

		self.__send_msg_to_topic('delivery_item_finished', from_status, to_status)
		process_order_after_delivery_item_service = ProcessOrderAfterDeliveryItemService.get(corp)
		process_order_after_delivery_item_service.process_order(self)

		return True, ''

	def ship(self, corp, with_logistics_trace, express_company_name_value, express_number, leader_name):
		"""
		影响:
		- 更新订单状态
		- 记录状态日志
		- 记录操作日志

		"""
		self.express_company_name_value = express_company_name_value
		self.express_number = express_number
		self.leader_name = leader_name
		self.with_logistics_trace = with_logistics_trace

		action_text = u'订单发货'
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_PAYED_SHIPED

		self.status = to_status

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)
		self.__save()

		self.__send_msg_to_topic('delivery_item_shipped', from_status, to_status)
		process_order_after_delivery_item_service = ProcessOrderAfterDeliveryItemService.get(corp)
		process_order_after_delivery_item_service.process_order(self)

		return True, ''

	def update_ship_info(self, corp, with_logistics_trace, express_company_name_value, express_number, leader_name):
		action_text = u'修改发货信息'
		self.express_company_name_value = express_company_name_value
		self.express_number = express_number
		self.leader_name = leader_name
		self.with_logistics_trace = with_logistics_trace

		self.__save()

		self.__send_msg_to_topic('delivery_item_ship_info_updated', self.status, self.status)

		self.__record_operation_log(self.bid, corp.username, action_text)
		return True, ''

	def apply_for_refunding(self, corp, cash, weizoom_card_money, coupon_money, integral):

		if self.status in (mall_models.ORDER_STATUS_GROUP_REFUNDING, mall_models.ORDER_STATUS_REFUNDING):
			return False, 'Error Status'

		action_text = u'退款'
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_REFUNDING

		self.status = to_status

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)

		if self.has_db_record:
			# 只有自营出货单开启高端退款（然而并不知道用什么词替代"高端"
			integral_strategy = corp.mall_config_repository.get_integral_strategy()
			integral_each_yuan = integral_strategy.integral_each_yuan
			integral_money = round(integral / integral_each_yuan, 2)

			total = cash + weizoom_card_money + coupon_money + integral_money

			self.refunding_info = {
				"cash": cash,
				"weizoom_card_money": weizoom_card_money,
				"coupon_money": coupon_money,
				"integral": integral,
				"integral_money": integral_money,
				"total": total,
				"finished": False
			}
		self.__save()

		self.__send_msg_to_topic('delivery_item_applied_for_refunding', from_status, to_status)
		process_order_after_delivery_item_service = ProcessOrderAfterDeliveryItemService.get(corp)
		process_order_after_delivery_item_service.process_order(self)

		return True, ''

	def refund(self, corp):
		if self.status not in (mall_models.ORDER_STATUS_REFUNDING, mall_models.ORDER_STATUS_GROUP_REFUNDING):
			return False, 'Error Status'
		action_text = u'退款完成'
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_REFUNDED

		self.status = to_status

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)

		if self.has_db_record:
			# 只有自营出货单开启高端退款（然而并不知道用什么词替代"高端"
			DeliveryItem.__fill_refunding_info([self], [self.id])

			self.refunding_info['finished'] = True

			# 更新订单的金额信息
			mall_models.Order.update(final_price=mall_models.Order.final_price - self.refunding_info['cash'],
			                         weizoom_card_money=mall_models.Order.weizoom_card_money - self.refunding_info[
				                         'weizoom_card_money']).dj_where(id=self.origin_order_id).execute()
		self.__save()

		self.__send_msg_to_topic('delivery_item_refunded', from_status, to_status)
		process_order_after_delivery_item_service = ProcessOrderAfterDeliveryItemService.get(corp)
		process_order_after_delivery_item_service.process_order(self)

		return True, ''

	def __record_operation_log(self, bid, operator_name, action_text):
		mall_models.OrderOperationLog.create(order_id=bid, operator=operator_name, action=action_text)

	def __recode_status_log(self, bid, operator_name, from_status, to_status):
		mall_models.OrderStatusLog.create(
			order_id=bid,
			from_status=from_status,
			to_status=to_status,
			operator=operator_name
		)

	def __send_msg_to_topic(self, msg_name, from_status, to_status):
		topic_name = TOPIC['delivery_item']
		data = {
			"delivery_item_id": self.id,
			"delivery_item_bid": self.bid,
			"corp_id": self.context['corp'].id,
			"from_status": mall_models.ORDER_STATUS2MEANINGFUL_WORD[from_status],
			"to_status": mall_models.ORDER_STATUS2MEANINGFUL_WORD[to_status]
		}
		logging.info('send mns message:{}'.format(data))
		msgutil.send_message(topic_name, msg_name, data)

	def __save(self):
		db_model = self.context['db_model']
		db_model.status = self.status
		db_model.payment_time = self.payment_time
		db_model.express_company_name = self.express_company_name_value
		db_model.express_number = self.express_number
		db_model.leader_name = self.leader_name
		db_model.is_100 = self.with_logistics_trace

		if self.refunding_info and self.refunding_info['finished'] is False:
			mall_models.OrderHasRefund.create(
				origin_order_id=self.origin_order_id,
				delivery_item_id=self.id,
				cash=self.refunding_info['cash'],
				weizoom_card_money=self.refunding_info['weizoom_card_money'],
				integral=self.refunding_info['integral'],
				integral_money=self.refunding_info['integral_money'],
				coupon_money=self.refunding_info['coupon_money'],
				total=self.refunding_info['total'],
				finished=False
			)
		elif self.refunding_info and self.refunding_info['finished'] is True:
			mall_models.OrderHasRefund.update(finished=True).dj_where(delivery_item_id=self.id).execute()

		db_model.save()

	def send_phone_message(self):

		if self.has_db_record:
			message_content = u"您好，订单号：%s，收货人：%s。已退单，请知晓！【微众传媒】"
			supplier_tel = self.supplier_info['supplier_tel']
			print '=============111===========================',supplier_tel	
			print '==============222==========================',message_content
			if supplier_tel:
				send_phone_captcha(supplier_tel, message_content % (self.bid, self.ship_name))
