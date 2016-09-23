# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from business.member.member import Member
from business.order.delivery_item import DeliveryItem
from db.mall import models as mall_models


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
		'raw_status',
		'status',
		'origin_order_id',
		'express_company_name',
		'express_number',
		'customer_message',
		'promotion_saved_money',

		'created_at',
		'update_at',

		'supplier',
		'integral_each_yuan',
		'webapp_id',
		'webapp_user_id',

		'weizoom_card_money',
		'delivery_time',  # 配送时间字符串
		'is_first_order',
		'supplier_user_id',
		'total_purchase_price',

		'member_info',
		'delivery_items',
		'is_self_order',
		'remark',
		'pay_money'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

	@staticmethod
	def from_models(args):
		db_models = args['db_models']
		fill_options = args['fill_options']
		# orders = [Order(db_model) for db_model in db_models]

		webapp_user_ids = []

		with_member = fill_options.get('with_member')
		with_delivery_items = fill_options.get('with_delivery_items') and fill_options['with_delivery_items']['fill']

		orders = []
		for db_model in db_models:
			order = Order()

			# 基本信息
			order.id = db_model.id
			order.bid = db_model.order_id  # todo 数据库层面处理bid
			order.bid_with_edit_money = order.bid + "-" + str(db_model.edit_money).replace('.', '').replace('-',
			                                                                                                '')  # 含有edit_money的bid
			order.status = db_model.status
			order.is_self_order = db_model.origin_order_id == -1  # todo 起个名
			order.remark = db_model.remark

			order.created_at = db_model.created_at
			# 支付信息
			order.pay_interface_type = db_model.pay_interface_type
			order.payment_time = db_model.payment_time

			# 金额信息
			order.final_price = db_model.final_price
			order.product_price = db_model.product_price
			order.edit_money = db_model.edit_money
			order.coupon_money = db_model.coupon_money

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

			order.delivery_items = []

			# 临时数据
			webapp_user_ids.append(db_model.webapp_user_id)
			order.context['db_model'] = db_model

			orders.append(order)

		if with_member:
			webapp_user_id2member, _ = Member.from_webapp_user_ids({'webapp_user_ids': webapp_user_ids})

		# if with_supplier:
		# 	webapp_user_id2member, _ = Member.from_webapp_user_ids({'webapp_user_ids': webapp_user_ids})

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
		print(1111)
		# 填充出货单
		if with_delivery_items:
			delivery_items_fill_options = fill_options['with_delivery_items']['fill_options']
			Order.fill_delivery_items(orders, delivery_items_fill_options)

		return orders

	@staticmethod
	def fill_delivery_items(orders, fill_options):
		# type: list(Order) -> None

		delivery_item_db_models = []
		order_ids = []

		self_order_ids = []
		for order in orders:
			order_ids.append(order.id)

			if order.is_self_order:
				self_order_ids.append(order.id)
			else:
				# 对于非拆单订单，出货单在db层即其本身
				delivery_item_db_models.append(order.context['db_model'])

		delivery_item_db_models.extend(mall_models.Order.select().dj_where(origin_order_id__in=self_order_ids))

		delivery_items = DeliveryItem.from_models({
			'models': delivery_item_db_models,
			'fill_options': fill_options
		})

		order_id2delivery_items = {}
		for item in delivery_items:
			if item.origin_order_id in order_id2delivery_items:
				order_id2delivery_items[item.origin_order_id].append(item)
			else:
				order_id2delivery_items[item.origin_order_id] = [item]

		for order in orders:
			order.delivery_items = order_id2delivery_items[order.id]  # todo

	def to_dict(self, *extras):

		result = business_model.Model.to_dict(self, *extras)
		if self.delivery_items:
			result['delivery_items'] = [delivery_item.to_dict() for delivery_item in self.delivery_items]

		return result
