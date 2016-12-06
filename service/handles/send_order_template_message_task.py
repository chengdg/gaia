# -*- coding: utf-8 -*-
"""

SELECT * from market_tools_template_message;
+------+------------+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+---------------------+
|   id |   industry | title                              |   send_point | attribute                                                                                                | created_at          |
|------+------------+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+---------------------|
|    1 |          1 | TM00247-购买成功通知               |            0 | product:product_name,price:final_price,time:payment_time                                                 | 2014-12-04 19:49:54 |
|    2 |          1 | OPENTM200303341-商品发货通知       |            1 | keyword1: express_company_name, keyword2:express_number, keyword3:product_name,keyword4:number           | 2014-12-04 19:49:54 |
|    3 |          0 | TM00398-付款成功通知               |            0 | orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id | 2014-12-04 19:49:54 |
|    4 |          0 | TM00505-订单标记发货通知           |            1 | orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id | 2014-12-04 19:49:54 |
|    5 |          0 | OPENTM200474379-优惠券领取成功通知 |            2 | keyword1:coupon_name,keyword3:invalid_date                                                               | 2015-09-25 17:52:48 |
|    6 |          0 | TM00853-优惠券过期提醒             |            3 | orderTicketStore:coupon_store,orderTicketRule:coupon_rule                                                | 2015-09-25 17:52:48 |
|    7 |          0 | OPENTM207449727-任务完成通知       |            4 | keyword1:task_name,keyword2:prize,keyword3:finish_time                                                   | 2016-01-28 20:53:07 |
+------+------------+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+---------------------+
"""

import settings
from bdem import msgutil
from business.mall.corporation import Corporation
from gaia_conf import TOPIC
from service.handler_register import register
from db.mall import models as mall_models

TEMPLATE_DB_TITLE2TMS_NAME = {
	u"TM00247-购买成功通知": u"购买成功通知",
	u"OPENTM200303341-商品发货通知": u"商品发货通知",
	u"TM00398-付款成功通知": u"付款成功通知",
	u"TM00505-订单标记发货通知": u"订单标记发货通知",
	u"OPENTM200474379-优惠券领取成功通知": u"优惠券领取成功通知",
	u"TM00853-优惠券过期提醒": u"优惠券过期提醒",
	u"OPENTM207449727-任务完成通知": u"任务完成通知"
}


@register("send_order_template_message_task")
def process(data, recv_msg=None):
	corp_id = data['corp_id']
	corp = Corporation(corp_id)
	to_status = data['to_status']
	topic = TOPIC['template_message']

	type = data['type']
	if type == 'delivery_item':
		delivery_item_id = data['delivery_item_id']

		fill_options = {'with_products': True}
		delivery_item = corp.delivery_item_repository.get_delivery_item(delivery_item_id, fill_options)

		order = corp.order_repository.get_order(delivery_item.origin_order_id, {'with_member': True})

		if to_status == 'shipped':
			send_point = mall_models.PAY_DELIVER_NOTIFY
			# todo 清理db model
			template_message_detail = mall_models.MarketToolsTemplateMessageDetail.select().join(
				mall_models.MarketToolsTemplateMessage).where(
				mall_models.MarketToolsTemplateMessageDetail.owner == corp_id,
				mall_models.MarketToolsTemplateMessage.send_point == send_point,
				mall_models.MarketToolsTemplateMessageDetail.status == 1).first()

			template_message = template_message_detail.template_message

			name = TEMPLATE_DB_TITLE2TMS_NAME[template_message.title]

			url = 'http://%s/mall/order_detail/?woid=%s&order_id=%s' % (
				settings.H5_DOMAIN, corp, order.bid)

			if template_message_detail:
				total_sale_price = u'￥%s［实际付款］' % delivery_item.product_statistics_info['total_sale_price']
				product_names = ','.join(delivery_item.product_statistics_info['product_names'])
				total_count = delivery_item.product_statistics_info['total_count']
				if name == u'商品发货通知':
					items = {
						'keyword1': delivery_item.express_company_name_text,
						'keyword2': delivery_item.express_number,
						'keyword3': product_names,
						'keyword4': total_count

					}
				elif name == u'订单标记发货通知':
					items = {
						'orderProductPrice': total_sale_price,
						'orderProductName': product_names,
						'orderName': order.bid,
						'orderAddress': delivery_item.ship_address

					}
				else:
					items = {}

				data = {
					'test_env': 'pttest',
					'user_id': corp.id,
					'member_id': order.member_info['id'],
					'name': name,
					'url': url,
					'items': items,
					'first': template_message_detail.first_text,
					'remark': template_message_detail.remark_text

				}
				msgutil.send_message(topic, 'template_msg', data)


# data = {
#
# 	'delivery_item_id':'1001435',
# 	'to_status':'shipped',
# 	'corp_id':490,
# 	'type':'delivery_item'
# }
# print(2222222222222)
# process(data,None)
