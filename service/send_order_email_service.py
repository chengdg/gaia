# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""
from service.service_register import register

# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from business.mall.corporation import Corporation
from business.order.service.paid_order_handle_service import PaidOrderHandleService
from service.service_register import register
from db.mall import models as mall_models




ORDER_STATUS2NOTIFY_STATUS = {
	mall_models.ORDER_STATUS_NOT: mall_models.PLACE_ORDER,
	mall_models.ORDER_STATUS_PAYED_NOT_SHIP: mall_models.PAY_ORDER,
	mall_models.ORDER_STATUS_PAYED_SHIPED: mall_models.SHIP_ORDER,
	mall_models.ORDER_STATUS_SUCCESSED: mall_models.SUCCESSED_ORDER,
	mall_models.ORDER_STATUS_CANCEL: mall_models.CANCEL_ORDER
}

@register("send_order_email")
def process(data, recv_msg=None):
	fill_options = {
		'with_delivery_items': {
			'with_products': True,
		}

	}
	order = self.corp.order_repository.get_order(order_id, fill_options)
	# 更新商品销量
	product_infos = []
	for item in order.delivery_items:
		product_infos.extend(item.products)
	# todo 赠品不计销量
	# for product in products:
	# 	if product.promotion != {'type_name': 'premium_sale:premium_product'}:
	# 		product_sale_infos.append({
	# 			'product_id': product.id,
	# 			'purchase_count': product.purchase_count
	# 		})
	for product_info in product_infos:
		product = self.corp.product_pool.get_products_by_ids([product_info.id])[0]

		product.update_sales(product_info.count)




	try:
		# print(self.ship_area)
		area = get_str_value_by_string_ids(self.ship_area)
	except:
		area = self.ship_area

	buyer_address = area + u" " + self.ship_address
	order_status = self.status_text

	email_notify_status = ORDER_STATUS2NOTIFY_STATUS.get(self.status, -1)
	try:
		member = self.context['webapp_user'].member
		if member is not None:
			member_id = member.id
		else:
			member_id = -1
	except:
		member_id = -1

	express_company_name = self.readable_express_company_name

	if self.express_number:
		express_number = self.express_number
	else:
		express_number = ''

	notify_order_mail.delay(
		user_id=self.context['webapp_owner'].id,
		member_id=member_id,
		status=email_notify_status,
		oid=self.id,
		order_id=self.order_id,
		buyed_time=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
		order_status=order_status,
		# buy_count=buy_count,
		total_price=self.final_price,
		bill='',
		coupon=self.coupon_id,
		coupon_money=self.coupon_money,
		# product_name=product_name,
		integral=self.integral,
		buyer_name=self.ship_name,
		buyer_address=buyer_address,
		buyer_tel=self.ship_tel,
		remark=self.customer_message,
		# product_pic_list=product_pic_list,
		postage=self.postage,
		express_company_name=express_company_name,
		express_number=express_number
	)
