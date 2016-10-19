# -*- coding: utf-8 -*-
from business import model as business_model
from db.mall import promotion_models
from eaglet.decorator import param_required


class CouponRule(business_model.Model):
	"""
	优惠券
	"""

	__slots__ = (
		'id',
		'name',
		'valid_days',
		'is_active',
		'start_date'
		'end_date',

		'valid_restrictions',
		'money',
		'count',
		'remained_count',
		'limit_counts',
		'limit_product',
		'limit_product_id',
		'remark',
		'get_person_count',
		'get_count',
		'use_count'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model

	@staticmethod
	@param_required(['db_model', 'corp'])
	def from_model(args):
		model = args['db_model']
		coupon_rule = CouponRule(model)
		coupon_rule._init_slot_from_model(model)
		coupon_rule.context['db_model'] = args['db_model']
		coupon_rule.context['corp'] = args['corp']
		return coupon_rule

	def update_use_count(self):
		promotion_models.CouponRule.update(use_count=promotion_models.CouponRule.use_count + 1).dj_where(
			id=self.id).execute()
