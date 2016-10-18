# -*- coding: utf-8 -*-

from business import model as business_model
from business.member.member import Member
from business.order.delivery_item import DeliveryItem
from db.mall import models as mall_models
from zeus_conf import TOPIC
from bdem import msgutil
from datetime import datetime, timedelta


class Order(business_model.Model):
	"""
	订单
	"""

	__slots__ = (
		'id',
		'bid',
		'type',
		'pay_interface_type',
		'payment_time',
		'final_price',
		'product_price',
		'edit_money',
		'bid_with_edit_money',

		'ship_name',
		'ship_tel',
		'ship_area',
		'ship_address',
		'bill_type',
		'bill',

		'postage',
		'integral',
		'integral_money',
		'coupon_money',

		'coupon_id',

		'status',

		'customer_message',

		'created_at',

		'webapp_id',
		'webapp_user_id',

		'weizoom_card_money',
		'delivery_time',  # 配送时间字符串
		'is_first_order',
		'supplier_user_id',
		'total_purchase_price',

		'delivery_items',
		'is_weizoom_order',
		'remark',
		'pay_money',
		'promotion_saved_money',

		# 他表数据
		'member_info',
		'is_group_buy',
		'refunding_info',
		'save_money',
		'origin_weizoom_card_money',
		'origin_final_price',
		'status_logs',
		'operation_logs',

		'is_second_generation_order'  # 对于第二代的同步订单，db层面出货单就是订单，此类订单不会再产生，业务只处理显示
	)

	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	def from_models(args):
		db_models = args['db_models']
		fill_options = args['fill_options']
		corp = args['corp']

		webapp_user_ids = []
		orders = []
		order_ids = []

		for db_model in db_models:
			order = Order()

			# 基本信息
			order.id = db_model.id
			order.bid = db_model.order_id  # todo 数据库层面处理bid
			if db_model.edit_money:
				order.bid_with_edit_money = order.bid + "-" + str(db_model.edit_money).replace('.', '').replace('-',
				                                                                                                '')  # 含有edit_money的bid
			else:
				order.bid_with_edit_money = order.bid
			order.status = db_model.status
			order.is_weizoom_order = db_model.origin_order_id == -1  # todo 起个名
			order.is_second_generation_order = db_model.origin_order_id > 0
			order.remark = db_model.remark
			order.type = db_model.type
			order.webapp_id = db_model.webapp_id
			order.webapp_user_id = db_model.webapp_user_id

			order.created_at = db_model.created_at
			# 支付信息
			order.pay_interface_type = db_model.pay_interface_type
			order.payment_time = db_model.payment_time

			# 金额信息
			order.final_price = db_model.final_price
			order.product_price = db_model.product_price
			order.edit_money = db_model.edit_money
			order.coupon_money = db_model.coupon_money
			order.postage = db_model.postage
			order.weizoom_card_money = db_model.weizoom_card_money
			order.integral_money = db_model.integral_money
			order.integral = db_model.integral
			order.promotion_saved_money = db_model.promotion_saved_money

			## 衍生数据
			order.pay_money = db_model.final_price + db_model.weizoom_card_money

			# 发票信息
			order.bill = db_model.bill
			order.bill_type = db_model.bill_type

			# 收货人信息
			order.ship_name = db_model.ship_name
			order.ship_tel = db_model.ship_tel
			order.ship_address = db_model.ship_address
			order.ship_area = db_model.ship_name

			# 会员信息
			order.webapp_user_id = db_model.webapp_user_id
			order.customer_message = db_model.customer_message

			# 出货单
			order.delivery_items = []

			# 其他信息
			order.delivery_time = db_model.delivery_time
			order.is_first_order = db_model.is_first_order

			# 临时数据
			webapp_user_ids.append(db_model.webapp_user_id)
			order.context['db_model'] = db_model
			order.context['corp'] = corp

			order_ids.append(db_model.id)

			orders.append(order)

		if fill_options and orders:
			with_member = fill_options.get('with_member')
			# with_delivery_items = fill_options.get('with_delivery_items')
			with_delivery_items = 'with_delivery_items' in fill_options
			with_group_buy_info = fill_options.get('with_group_buy_info')
			with_refunding_info = fill_options.get('with_refunding_info')
			with_full_money_info = fill_options.get('with_full_money_info')  # 有依赖
			with_status_logs = fill_options.get('with_status_logs')
			with_operation_logs = fill_options.get('with_operation_logs')

			if with_member:
				webapp_user_id2member, _ = Member.from_webapp_user_ids({'webapp_user_ids': webapp_user_ids})
			else:
				webapp_user_id2member = {}

			for order in orders:

				if with_member:
					member = webapp_user_id2member.get(order.webapp_user_id, None)
					if member:
						order.member_info = {
							'name': member.username_for_html,
							'id': member.id,
							'is_subscribed': member.is_subscribed
						}
					else:
						order.member_info = {
							'name': u'未知',
							'id': 0,
							'is_subscribed': 0
						}

			# 填充出货单
			if with_delivery_items:
				delivery_items_fill_options = fill_options['with_delivery_items']
				Order.__fill_delivery_items(orders, delivery_items_fill_options)

			if with_group_buy_info:
				Order.__fill_group_buy(orders, order_ids)

			if with_refunding_info:
				Order.__fill_refunding_info(orders, order_ids)

			if with_full_money_info:
				# 需要在最后
				Order.__fill_full_money_info(orders, order_ids)

			if with_status_logs:
				Order.__fill_status_logs(orders, order_ids)

			if with_operation_logs:
				Order.__fill_operation_logs(orders, order_ids)

		return orders

	@staticmethod
	def __fill_delivery_items(orders, fill_options):
		"""
		填充出货单信息
		@param orders:
		@param fill_options:
		@return:
		"""
		# type: list(Order) -> None

		delivery_item_db_models = []
		order_ids = []
		if len(orders):
			corp = orders[0].context['corp']
		else:
			corp = None

		self_order_ids = []
		for order in orders:
			order_ids.append(order.id)

			if order.is_weizoom_order:
				self_order_ids.append(order.id)
			elif order.is_second_generation_order:
				# 对于老同步订单，出货单在db层是出货单本身
				delivery_item_db_models.append(order.context['db_model'])
			else:
				# 对于非拆单订单，出货单在db层即其本身
				delivery_item_db_models.append(order.context['db_model'])

		delivery_item_db_models.extend(mall_models.Order.select().dj_where(origin_order_id__in=self_order_ids))

		delivery_items = DeliveryItem.from_models({
			'models': delivery_item_db_models,
			'fill_options': fill_options,
			'corp': corp
		})

		order_id2delivery_items = {}
		for item in delivery_items:
			if item.origin_order_id in order_id2delivery_items:
				order_id2delivery_items[item.origin_order_id].append(item)
			else:
				order_id2delivery_items[item.origin_order_id] = [item]

		for order in orders:
			order.delivery_items = order_id2delivery_items[order.id]

	@staticmethod
	def __fill_status_logs(orders, order_ids):
		logs = mall_models.OrderStatusLog.select().dj_where(order_id__in=order_ids).order_by(
			mall_models.OrderStatusLog.created_at)
		if len(orders) == 1:
			order = orders[0]
			order.status_logs = []
			# 下单时没状态日志
			order.status_logs.append({'status': mall_models.ORDER_STATUS_NOT, 'time': order.created_at})
			for log in logs:
				order.status_logs.append({'status': log.to_staus, 'time': log.created_at})

	@staticmethod
	def __fill_group_buy(orders, order_ids):
		"""
		填充团购信息
		@param orders:
		@param order_ids:
		@return:
		"""
		bids = [order.bid for order in orders]
		group_infos = mall_models.OrderHasGroup.select().dj_where(order_id__in=bids)

		bid2group_info = {group_info.order_id: group_info for group_info in group_infos}

		for order in orders:
			order.is_group_buy = bool(bid2group_info.get(order.bid))

	@staticmethod
	def __fill_refunding_info(orders, order_ids):
		for order in orders:
			if order.is_weizoom_order:
				order.refunding_info = {
					'cash': sum([delivery_item.refund_info['cash'] for delivery_item in order.delivery_items if
					             delivery_item.refund_info['finished']]),
					'weizoom_card_money': sum(
						[delivery_item.refund_info['weizoom_card_money'] for delivery_item in order.delivery_items if
						 delivery_item.refund_info['finished']]),
					'integral_money': sum(
						[delivery_item.refund_info['integral_money'] for delivery_item in order.delivery_items if
						 delivery_item.refund_info['finished']]),
					'integral': sum(
						[delivery_item.refund_info['integral'] for delivery_item in order.delivery_items if
						 delivery_item.refund_info['finished']]),
					'coupon_money': sum(
						[delivery_item.refund_info['coupon_money'] for delivery_item in order.delivery_items if
						 delivery_item.refund_info['finished']]),
					'total': sum([delivery_item.refund_info['total'] for delivery_item in order.delivery_items if
					              delivery_item.refund_info['finished']]),
				}
			else:
				order.refunding_info = {
					'cash': 0,
					'weizoom_card_money': 0,
					'integral': 0,
					'integral_money': 0,
					'coupon_money': 0,
					'total': 0,
				}

	@staticmethod
	def __fill_full_money_info(orders, order_ids):

		for order in orders:
			order.origin_weizoom_card_money = order.weizoom_card_money + order.refunding_info[
				'weizoom_card_money']
			order.origin_final_price = order.final_price + order.refunding_info['cash']

			total_product_origin_price = sum(
				[delivery_item.total_origin_product_price for delivery_item in order.delivery_items])

			order.save_money = round(total_product_origin_price, 2) + round(order.postage, 2) - round(
				order.origin_final_price,
				2) - round(
				order.origin_weizoom_card_money, 2)

	@staticmethod
	def __fill_operation_logs(orders, order_ids):

		if len(orders) == 1:
			order = orders[0]

			logs = mall_models.OrderOperationLog.select().dj_where(order_id=order.bid)
			order.operation_logs = []
			for log in logs:
				order.operation_logs.append({
					'action_text': log.action,
					'time': log.created_at,
					'operator': log.operator
				})


	def to_dict(self, *extras):
		result = business_model.Model.to_dict(self, *extras)
		if self.delivery_items:
			result['delivery_items'] = [delivery_item.to_dict() for delivery_item in self.delivery_items]

		return result

	def update_final_price(self, corp, new_final_price):
		"""
		修改价格
		@param corp:
		@param new_final_price:
		@return:
		"""
		if self.status != mall_models.ORDER_STATUS_NOT:
			return False, 'Error Status'
		if self.final_price != new_final_price:
			action_text = u' 修改订单金额'
			db_model = self.context['db_model']

			self.final_price = new_final_price
			self.edit_money = (db_model.product_price + db_model.postage) - (
				db_model.coupon_money + db_model.integral_money + db_model.weizoom_card_money + db_model.promotion_saved_money) - new_final_price

			self.__save()

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__send_msg_to_topic('update_order_final_price')
			return True, ''
		else:
			return True, ''

	def update_remark(self, corp, new_remark):
		if self.remark != new_remark:
			self.remark = new_remark
			action_text = u' 修改订单备注'

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__save()
			return True, ''

	def pay(self, corp):
		"""
		影响：
		- 更新订单状态
		- 更新支付时间
		- 更新买家的首单信息
		- 支付出货单
		- 记录状态日志
		- 记录操作日志

		- 更新会员信息
		- 更新销量
		- 发送模板消息
		- 发送运营邮件通知
		@param corp:
		@return:
		"""
		if self.status != mall_models.ORDER_STATUS_NOT:
			return False, 'Error Status'

		action_text = u"支付"
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_PAYED_NOT_SHIP
		payment_time = datetime.now()

		self.status = to_status
		self.payment_time = payment_time

		# 更新首单信息
		if mall_models.Order.select().dj_where(
				webapp_id=self.webapp_id,
				webapp_user_id=self.webapp_user_id,
				is_first_order=True).count() == 0:
			self.is_first_order = True

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)
		self.__save()

		Order.__fill_delivery_items([self], None)

		for delivery_item in self.delivery_items:
			delivery_item.pay(payment_time, corp)

		self.__send_msg_to_topic('pay_order')
		print('---send pay order message')
		return True, ''

	def cancel(self, corp):
		"""
		影响:
		- 更新订单状态
		- 记录状态日志
		- 记录操作日志
		- 取消出货单


		- 返还订单资源
			- 积分
			- 优惠券
			- 库存
			- 微众卡
			- 库存
		- 更新商品销量（如果订单已支付
		- 更新会员信息
		- 发送运营邮件通知
		- 发送短信通知

		@return:
		"""
		action_text = u"取消订单"
		from_status = self.status
		to_status = mall_models.ORDER_STATUS_CANCEL
		self.status = to_status

		self.__record_operation_log(self.bid, corp.username, action_text)
		self.__recode_status_log(self.bid, corp.username, from_status, to_status)
		self.__save()

		Order.__fill_delivery_items([self], None)

		for delivery_item in self.delivery_items:
			delivery_item.cancel(corp)

		self.__send_msg_to_topic('cancel_order')
		return True, ''

	def finish(self, corp, only_send_message):
		"""
		只会由出货单都完成触发
		@param only_send_message:
		@param corp:
		@return:
		"""
		if not only_send_message:
			action_text = u"完成"
			from_status = self.status
			to_status = mall_models.ORDER_STATUS_SUCCESSED
			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('finish_order')
		return True, ''

	def ship(self, corp, only_send_message):
		"""
		只会由出货单都完成触发
		@param only_send_message:
		@param corp:
		@return:
		"""
		if not only_send_message:
			action_text = u"订单发货"
			from_status = self.status
			to_status = mall_models.ORDER_STATUS_PAYED_SHIPED
			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('ship_order')
		return True, ''

	def apply_for_refunding(self, corp, only_send_message):
		"""
		只会由出货单都完成触发
		@param only_send_message:
		@param corp:
		@return:
		"""
		if not only_send_message:
			action_text = u"退款"
			from_status = self.status
			to_status = mall_models.ORDER_STATUS_REFUNDING
			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('apply_for_refunding_order')
		return True, ''

	def refund(self, corp, only_send_message):
		"""

		@param corp:
		@param only_send_message:
		@return:
		"""
		if not only_send_message:
			action_text = u"退款完成"
			from_status = self.status
			to_status = mall_models.ORDER_STATUS_REFUNDING
			self.status = to_status

			self.__record_operation_log(self.bid, corp.username, action_text)
			self.__recode_status_log(self.bid, corp.username, from_status, to_status)
			self.__save()

		self.__send_msg_to_topic('refund_order')
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
		topic_name = TOPIC['order']
		data = {
			"order_id": self.id,
			"order_bid": self.bid,
			"corp_id": self.context['corp'].id
		}
		msgutil.send_message(topic_name, msg_name, data)

	def __save(self):
		"""
		持久化修改的数据
		@return:
		"""
		db_model = self.context['db_model']
		db_model.status = self.status
		db_model.payment_time = self.payment_time
		db_model.is_first_order = self.is_first_order
		db_model.remark = self.remark
		db_model.save()
