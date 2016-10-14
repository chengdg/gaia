# -*- coding: utf-8 -*-
"""
出货单
"""
from bdem import msgutil
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.supplier import Supplier
from business.order.delivery_item_product_repository import DeliveryItemProductRepository
from business.order.process_order_after_delivery_item_service import ProcessOrderAfterDeliveryItemService
from db.express import models as express_models
from db.mall import models as mall_models
from zeus_conf import TOPIC


class DeliveryItem(business_model.Model):
	__slots__ = (
		'id',
		'bid',
		'origin_order_id',
		'products',

		'postage',
		'status',
		'express_company_name',
		'express_number',
		'leader_name',
		'created_at',
		'payment_time',

		'refunding_info',
		'total_origin_product_price',
		'supplier_info',
		'express_details',
		'is_use_delivery_item_db_model',  # 出货单使用出货单db，即db层面有出货单
		'with_logistics_trace',  # 是否使用快递100，对应于数据库里的is_100
		'with_logistics'         # 是否使用物流
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.id = db_model.id
		self.bid = db_model.order_id

		if db_model.origin_order_id > 0:
			self.origin_order_id = db_model.origin_order_id
		else:
			self.origin_order_id = db_model.id

		self.is_use_delivery_item_db_model = db_model.origin_order_id > 0  # 出货单使用出货单db，即db层面有出货单

		self.postage = db_model.postage

		self.status = db_model.status
		self.payment_time = db_model.payment_time

		# 快递公司信息
		self.express_company_name = db_model.express_company_name
		self.express_number = db_model.express_number
		self.leader_name = db_model.leader_name
		self.created_at = db_model.created_at
		self.with_logistics_trace = db_model.is_100
		self.with_logistics = bool(db_model.express_company_name)
		self.context['db_model'] = db_model

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
			express_company_names = []
			express_numbers = []
			for delivery_item in delivery_items:
				express_company_names.append(delivery_item.express_company_name)
				express_numbers.append(delivery_item.express_number)

				delivery_item.express_details = []

			express_push_list = express_models.ExpressHasOrderPushStatus.select().dj_where(
				express_company_name__in=express_company_names,
				express_number__in=express_numbers
			)

			name_number2express_push_id = {str(push.express_company_name + '__' + push.express_number): push.id for push
			                               in express_push_list}

			express_push_ids = []
			for push in express_push_list:
				express_push_ids.append(push.id)

			express_details = express_models.ExpressDetail.select().dj_where(express_id__in=express_push_ids)
			express_push_id2details = {detail.express_id: detail for detail in express_details}

			for detail in express_details:
				if detail.express_id in express_push_id2details:
					express_push_id2details[detail.express_id].append(detail)
				else:
					express_push_id2details[detail.express_id] = [detail]

			for delivery_item in delivery_items:
				push_id = name_number2express_push_id.get(
					str(delivery_item.express_company_name + '__' + delivery_item.express_number))
				if push_id:
					express_details = express_push_id2details.get(push_id, [])

					for detail in express_details:
						delivery_item.express_details.append({
							'ftime': detail.ftime,
							'context': detail.context
						})

	@staticmethod
	def __fill_products(delivery_items):
		# delivery_items_products = DeliveryItemsProducts.get_for_delivery_items(delivery_items=delivery_items,
		#                                                                        with_premium_sale=True)
		if delivery_items:
			corp = delivery_items[0].context['corp']
		else:
			corp = None
		delivery_item_product_repository = DeliveryItemProductRepository.get({'corp': corp})

		delivery_items_products = delivery_item_product_repository.get_products_for_delivery_items(
			delivery_items=delivery_items,
			with_premium_sale=True)

		delivery_item_id2products = {}
		for product in delivery_items_products:
			if product.delivery_item_id in delivery_item_id2products:
				delivery_item_id2products[product.delivery_item_id].append(product)
			else:
				delivery_item_id2products[product.delivery_item_id] = [product]

		for delivery_item in delivery_items:
			delivery_item.products = delivery_item_id2products[delivery_item.id]
			delivery_item.total_origin_product_price = sum([p.total_origin_price for p in delivery_item.products])

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
			refunding_info = delivery_item_id2refund_info.get(delivery_item.id)
			if refunding_info:
				delivery_item.refunding_info = {
					'cash': refunding_info.cash,
					'weizoom_card_money': refunding_info.weizoom_card_money,
					'integral': refunding_info.integral,
					'integral_money': refunding_info.integral_money,
					'coupon_money': refunding_info.coupon_money,
					'total': refunding_info.total,
					'finished': refunding_info.finished
				}
			else:
				delivery_item.refunding_info = {
					'cash': 0,
					'weizoom_card_money': 0,
					'integral': 0,
					'integral_money': 0,
					'coupon_money': 0,
					'total': 0,
					'finished': False
				}

	@staticmethod
	def __fill_supplier(delivery_items, delivery_item_ids):
		# todo 性能优化
		for delivery_item in delivery_items:
			db_model = delivery_item.context['db_model']
			supplier = None
			if db_model.supplier_user_id:
				supplier = Supplier.from_id({
					'id': db_model.supplier_user_id,
					'type': 'user'
				})
			elif db_model.supplier:
				supplier = Supplier.from_id({
					'id': db_model.supplier_user_id,
					'type': 'supplier'
				})

			if supplier:
				delivery_item.supplier_info = {
					'name': supplier.name,
					'type': supplier.type
				}
			else:
				delivery_item.supplier_info = {

				}

	def pay(self, payment_time, corp):
		"""
		支付出货单，只由pay_order触发
		@return:
		"""

		if self.is_use_delivery_item_db_model:
			action_text = u"支付"
			from_status = self.status
			to_status = mall_models.ORDER_STATUS_PAYED_NOT_SHIP

			self.payment_time = payment_time
			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('pay_delivery_item')

	def cancel(self, corp):
		"""
		取消出货单，只有cancel_order触发
		@param corp:
		@return:
		"""
		if self.is_use_delivery_item_db_model:
			action_text = u"支付"
			from_status = self.status
			to_status = mall_models.ORDER_STATUS_PAYED_NOT_SHIP

			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('cancel_delivery_item')

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

		action_text = u'完成'
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_SUCCESSED

		self.status = to_status

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)
		self.__save()

		self.__send_msg_to_topic('finish_delivery_item')
		process_order_after_delivery_item_service = ProcessOrderAfterDeliveryItemService.get(corp)
		process_order_after_delivery_item_service.process_order(self)

		return True, ''

	def ship(self, corp, with_logistics_trace, company_name_value, express_number, leader_name):
		"""
		影响:
		- 更新订单状态
		- 记录状态日志
		- 记录操作日志

		@param corp:
		@param express_company_name:
		@param express_number:
		@param leader_name:
		@param is_100:
		@return:
		"""
		self.express_company_name = company_name_value
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

		self.__send_msg_to_topic('ship_delivery_item')
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

	def __send_msg_to_topic(self, msg_name):
		topic_name = TOPIC['delivery_item']
		data = {
			"delivery_item_id": self.id,
			"delivery_item_bid": self.bid
		}
		msgutil.send_message(topic_name, msg_name, data)

	def __save(self):
		db_model = self.context['db_model']
		db_model.status = self.status
		db_model.payment_time = self.payment_time
		db_model.express_company_name = self.express_company_name
		db_model.express_number = self.express_number
		db_model.leader_name = self.leader_name
		db_model.is_100 = self.with_logistics_trace
		db_model.save()
