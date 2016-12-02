# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""
import time

from eaglet.core.sendmail import sendmail

import settings
from business.mall.notify.notification_repository import NotificationRepository
from service.handler_register import register

# -*- coding: utf-8 -*-
from util.regional_util import get_str_value_by_string_ids

from business.mall.corporation import Corporation
from service.handler_register import register
from db.mall import models as mall_models

ORDER_STATUS2NOTIFY_STATUS = {
	mall_models.ORDER_STATUS_NOT: mall_models.PLACE_ORDER,
	mall_models.ORDER_STATUS_PAYED_NOT_SHIP: mall_models.PAY_ORDER,
	mall_models.ORDER_STATUS_PAYED_SHIPED: mall_models.SHIP_ORDER,
	mall_models.ORDER_STATUS_SUCCESSED: mall_models.SUCCESSED_ORDER,
	mall_models.ORDER_STATUS_CANCEL: mall_models.CANCEL_ORDER
}


def __send_email(emails, content_described, content):
	for email in emails:
		print('-----emails', email, content_described, content)
		sendmail(email, content_described, content)


@register("send_order_email_task")
def process(data, recv_msg=None):
	return
	# 暂时停用
	type = data['type']
	if type == 'order':
		corp_id = data['corp_id']
		order_id = data['order_id']

		corp = Corporation(corp_id)

		fill_options = {
			'with_member': True,
			'with_delivery_items': {
				'with_products': True,

			}

		}

		order = corp.order_repository.get_order(order_id, fill_options)
		# 更新商品销量
		delivery_item_products = []
		for item in order.delivery_items:
			delivery_item_products.extend(item.products)

		notification_repository = NotificationRepository.get(corp)
		order_notify_type = ORDER_STATUS2NOTIFY_STATUS.get(order.status, -1)
		order_notify = notification_repository.get_email_notification_by_type(order_notify_type)

		if order_notify and order_notify.is_active and order.member_info[
			'id'] not in order_notify.black_member_ids and order_notify.email_addresses:
			buy_count = ''
			product_name = ''
			product_pic_list = []
			for delivery_item_product in delivery_item_products:
				buy_count = buy_count + str(delivery_item_product.count) + ','
				product_name = product_name + delivery_item_product.name + ','
				product_pic_list.append(delivery_item_product.thumbnails_url)
			buy_count = buy_count[:-1]
			product_name = product_name[:-1]

			content_list = []
			content_described = u'微商城-%s-订单' % order.status_text
			if order_id:
				if product_name:
					content_list.append(u'商品名称：%s' % product_name)
				if product_pic_list:
					pic_address = ''
					for pic in product_pic_list:
						if pic.find('http') < 0:
							pic = "http://%s%s" % (settings.HERMES_DOMAIN, pic)
						pic_address = pic_address + "<img src='%s' width='170px' height='200px'></img>" % (pic)
					if pic_address != '':
						content_list.append(pic_address)
				content_list.append(u'订单号：%s' % order_id)

				content_list.append(u'下单时间：%s' % time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))

				content_list.append(u'订单状态：<font color="red">%s</font>' % order.status_text)

				# 从拆单之后，此处是未定义行为
				# express_company_name = corp.express_delivery_repository.get_company_by_value(order.ex)
				# express_company_name = 'xx' # todo
				# if express_company_name:
				# 	content_list.append(u'<font color="red">物流公司：%s</font>' % express_company_name)
				# if order.express_number:
				# 	content_list.append(u'<font color="red">物流单号：%s</font>' % order.express_number)
				if buy_count:
					content_list.append(u'订购数量：%s' % buy_count)
				if order.final_price:
					content_list.append(u'支付金额：%s' % order.final_price)
				if order.integral:
					content_list.append(u'使用积分：%s' % order.integral)
				if order.coupon_id:
					content_list.append(u'优惠券：%s' % order.coupon_id)

				if order.postage:
					content_list.append(u'邮费：%s' % order.postage)

				content_list.append(u'收货人：%s' % order.ship_name)

				content_list.append(u'收货人电话：%s' % order.ship_tel)

				# area = get_str_value_by_string_ids(order.ship_area)
				area = ""
				buyer_address = area + u" " + order.ship_address
				content_list.append(u'收货人地址：%s' % buyer_address)
				# if order.customer_message:
				# 	content_list.append(u'顾客留言：%s' % order.customer_message)

			content = u'<br> '.join(content_list)
			try:
				__send_email(order_notify.email_addresses, content_described, content)
			except:
				from eaglet.core.exceptionutil import unicode_full_stack
				from eaglet.core import watchdog
				watchdog.alert({
					'uuid': "send_email_error",
					'traceback': unicode_full_stack(),
					'email_addresses': order_notify.email_addresses
				})
				pass
	else:
		# todo
		pass
