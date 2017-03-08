# -*- coding: utf-8 -*-
import random

from business import model as business_model
from business.coupon.coupon import Coupon
from db.mall import promotion_models
from eaglet.decorator import param_required
from business import model as business_model
from business.coupon.coupon import Coupon


class CouponFactory(business_model.Service):
	def __generate_new_coupon_id(self, coupon_rule, exist_coupon_ids):
		"""
		生成coupon_rule中一个新的coupon id
		"""
		a = int(coupon_rule.owner_id)
		b = int(coupon_rule.id)
		coupon_id = self.__generate_next_coupon_id(a, b)
		while coupon_id in exist_coupon_ids:
			coupon_id = self.__generate_next_coupon_id(a, b)

		return coupon_id		

	def __generate_next_coupon_id(self, a, b):
		random_args_value = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
		return '%03d%04d%s' % (a, b, ''.join(random.sample(random_args_value, 6)))

	def create_coupons_for_rule(self, coupon_rule, count):
		# 创建未使用的优惠券
		current_coupon_id_set = set([coupon.coupon_id for coupon in promotion_models.Coupon.select().dj_where(coupon_rule_id=coupon_rule.id)])
		coupons = []
		i = 0
		while i < count:
			coupon_id = self.__generate_new_coupon_id(coupon_rule, current_coupon_id_set)

			current_coupon_id_set.add(coupon_id)
			model = promotion_models.Coupon.create(
				owner = coupon_rule.owner_id,
				coupon_id = coupon_id,
				start_time = coupon_rule.start_date,
				expired_time = coupon_rule.end_date,
				money = coupon_rule.money,
				coupon_rule = coupon_rule.id,
				is_manual_generated = False,
				status = promotion_models.COUPON_STATUS_UNGOT
			)
			i += 1

			coupons.append(Coupon(model))