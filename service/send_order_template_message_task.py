# -*- coding: utf-8 -*-
"""
处理已支付的订单
"""
import time

from eaglet.core.sendmail import sendmail

import settings
from business.mall.notify.notification_repository import NotificationRepository
from service.service_register import register

# -*- coding: utf-8 -*-
from util.regional_util import get_str_value_by_string_ids

"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from business.mall.corporation import Corporation
from service.service_register import register
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
		sendmail(email, content_described, content)


@register("send_order_template_task")
def process(data, recv_msg=None):
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

	# todo

	# webapp_owner = self.context['webapp_owner']
	# webapp_user = self.context['webapp_user']
	# # user_profile = UserProfile.objects.get(webapp_id=webapp_id)
	# user_profile = webapp_owner.user_profile
	# user = user_profile.user
	# send_point = ORDER_STATUS2SEND_PONINT.get(self.status, '')
	# # template_message = mall_models.MarketToolsTemplateMessageDetail.select().dj_where(owner=user, template_message__send_point=send_point, status=1).first()
	# template_message = mall_models.MarketToolsTemplateMessageDetail.select().join(
	# 	mall_models.MarketToolsTemplateMessage).where(mall_models.MarketToolsTemplateMessageDetail.owner == user,
	#                                                   mall_models.MarketToolsTemplateMessage.send_point == send_point,
	#                                                   mall_models.MarketToolsTemplateMessageDetail.status == 1).first()
	#
	# if user_profile and template_message and template_message.template_id:
	# 	mpuser_access_token = webapp_owner.weixin_mp_user_access_token
	# 	if mpuser_access_token:
	# 		try:
	# 			message = self.__get_order_send_message_dict(user_profile, template_message, self, send_point)
	#
	# 			mpuser_access_token_dict = mpuser_access_token.to_dict()
	#
	# 			del mpuser_access_token_dict['update_time']
	# 			del mpuser_access_token_dict['expire_time']
	# 			del mpuser_access_token_dict['created_at']
	# 			send_template_message.delay(mpuser_access_token_dict, message)
	# 			return True
	# 		except:
	# 			notify_message = u"发送模板消息异常, cause:\n{}".format(unicode_full_stack())
	# 			watchdog.warning(notify_message)
	# 			return False
	# 	else:
	# 		return False
	# return True


