# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

from bdem import msgutil

from business.mall.corporation import Corporation
from business.member.member_spread import MemberSpread
from service.handler_register import register
from gaia_conf import TOPIC
from service.utils import not_retry
from db.mall import promotion_models as promotion_models

@register("order_finished")
@not_retry
def process(data, recv_msg=None):
	"""
	处理支付订单消息
	"""
	corp_id = data['corp_id']
	order_id = data['order_id']
	from_status = data['from_status']
	to_status = data['to_status']

	corp = Corporation(corp_id)

	fill_options = {
		'with_member': True,
		'with_delivery_items': {
			'with_products': True,
		}

	}
	order = corp.order_repository.get_order(order_id, fill_options)
	# 更新商品销量

	# todo 赠品不计销量
	# for product in products:
	# 	if product.promotion != {'type_name': 'premium_sale:premium_product'}:
	# 		product_sale_infos.append({
	# 			'product_id': product.id,
	# 			'purchase_count': product.purchase_count
	# 		})

	# # 发送运营邮件通知
	# topic_name = TOPIC['base_service']
	# data = {
	# 	"type": "order",
	# 	"order_id": order.id,
	# 	"corp_id": corp.id
	# }
	# msgutil.send_message(topic_name, 'send_order_email_task', data)

	# 发送模板消息
	topic_name = TOPIC['base_service']
	data = {
		"order_id": order.id,
		"corp_id": corp.id
	}
	msgutil.send_message(topic_name, 'send_order_template_message_task', data)

	member = corp.member_repository.get_member_by_id(order.member_info['id'])

	member.increase_integral_after_finish_order(order)  # 对应购买商品返积分功能
	member.update_pay_info(order, from_status, to_status)
	MemberSpread.process_order_from_spread({'order_id': order.id})

	# 更新红包引入消费金额的数据
	if order.coupon_id and promotion_models.RedEnvelopeParticipences.select().dj_where(coupon_id=order.coupon_id,
	                                                                                  introduced_by__gt=0).count() > 0:
		red_envelope2member = promotion_models.RedEnvelopeParticipences.select().dj_where(
			coupon_id=order.coupon_id).first()
		promotion_models.RedEnvelopeParticipences.update(
			introduce_sales_number=promotion_models.RedEnvelopeParticipences.introduce_sales_number + order.final_price + order.postage).dj_where(
			red_envelope_rule_id=red_envelope2member.red_envelope_rule_id,
			red_envelope_relation_id=red_envelope2member.red_envelope_relation_id,
			member_id=red_envelope2member.introduced_by
		).execute()



