# -*- coding: utf-8 -*-
"""@package business.mall.coupon
优惠券
"""
from datetime import datetime

from business import model as business_model
from db.mall import promotion_models
from db.mall import models as mall_models
from eaglet.decorator import param_required
from business.mall.corporation_factory import CorporationFactory

DEFAULT_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')

class Coupon(business_model.Model):
	"""
	优惠券
	"""

	__slots__ = (
		'id',
		'bid',
		'status',
		'display_status',
		'start_time',
		'expired_time',
		'created_at',
		'received_time',
		'used_time',
		'money',
		'member',
		'order_bid', #订单的bid
		'receive_user_name', #领取人
		'use_user_name' #使用人
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.bid = model.coupon_id
			self.display_status = promotion_models.COUPONSTATUS2STR[model.status]
			self.received_time = model.provided_time
			self.used_time = DEFAULT_DATETIME
			self.use_user_name = u'默认使用人'
			self.receive_user_name = u'默认领取人'
			self.order_bid = ''


	@property
	def rule(self):
		if not '_rule' in self.context:
			corp = CorporationFactory.get()
			db_model = self.context['db_model']
			self.context['_rule'] = corp.coupon_rule_repository.get_coupon_rule_by_id(db_model.coupon_rule_id)

		return self.context['_rule']

	@property
	def using_limit(self):
		return self.rule.using_limit

	def refund(self,order):
		"""
		取消、退款订单时返还优惠券
		"""
		if self.received_time == promotion_models.DEFAULT_DATETIME:
			self.status = promotion_models.COUPON_STATUS_UNGOT
		else:
			self.status = promotion_models.COUPON_STATUS_UNUSED
		promotion_models.Coupon.update(status=self.status).dj_where(id=self.id).update()
		self.rule.update_use_count(-1) #更新coupon rule中记录的数量
		
		# 更新红包优惠券分析数据 by Eugene
		if promotion_models.RedEnvelopeParticipences.select().dj_where(coupon_id=self.id,
		                                                            introduced_by__gt=0).count() > 0:

			red_envelope2member = promotion_models.RedEnvelopeParticipences.select().dj_where(
				coupon_id=order.coupon_id).first()

			if red_envelope2member:
				promotion_models.RedEnvelopeParticipences.update(
					introduce_used_number=promotion_models.RedEnvelopeParticipences.introduce_used_number + 1).dj_where(
					red_envelope_rule_id=red_envelope2member.red_envelope_rule_id,
					red_envelope_relation_id=red_envelope2member.red_envelope_relation_id,
					member_id=red_envelope2member.introduced_by
				).execute()

			if order.status >= mall_models.ORDER_STATUS_SUCCESSED:

				promotion_models.RedEnvelopeParticipences.update(
					introduce_sales_number=promotion_models.RedEnvelopeParticipences.introduce_sales_number - order.final_price - order.postage).dj_where(
					red_envelope_rule_id=red_envelope2member.red_envelope_rule_id,
					red_envelope_relation_id=red_envelope2member.red_envelope_relation_id,
					member_id=red_envelope2member.introduced_by
				).execute()

