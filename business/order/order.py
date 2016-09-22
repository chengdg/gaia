# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from business.member.member import Member
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
		'member_grade_id',
		'member_grade_discount',
		'buyer_name',

		'weizoom_card_money',
		'delivery_time',  # 配送时间字符串
		'is_first_order',
		'supplier_user_id',
		'total_purchase_price',
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

	@staticmethod
	def fill_orders(args):
		db_models = args['db_models']
		fill_options = args['fill_options']
		# orders = [Order(db_model) for db_model in db_models]

		webapp_user_ids = []

		with_member = fill_options.get('with_member')

		orders = []
		for db_model in db_models:
			order = Order()

			# 基本信息
			order.id = db_model.id
			order.bid = db_model.order_id  # todo 数据库层面处理bid
			order.bid_with_edit_money = order.bid + "-" + str(db_model.edit_money).replace('.', '').replace('-',
			                                                                                                '')  # 含有edit_money的bid
			order.created_at = db_model.created_at
			# 支付信息
			order.pay_interface_type = db_model.pay_interface_type
			order.payment_time = db_model.payment_time

			# 金额信息
			order.final_price = db_model.final_price
			order.product_price = db_model.product_price
			order.edit_money = db_model.edit_money
			order.coupon_money = db_model.coupon_money

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

			# 临时数据
			webapp_user_ids.append(db_model.webapp_user_id)

			orders.append(order)

		if with_member:
			webappuser_id2member, _ = Member.from_webapp_user_ids({'webapp_user_ids': webapp_user_ids})

		for order in orders:


			if with_member:
				order.member_info = webappuser_id2member[order.webapp_user_id].to_dict()

		return orders
