# -*- coding: utf-8 -*-
"""@package business.mall.promotion.integral_sale_rule
积分应用规则，在积分应用中，我们可以为每个等级的会员设定一个积分应用规则

"""
from business import model as business_model


class IntegralSaleRule(business_model.Model):
	"""
	积分应用
	"""
	__slots__ = (
		'id',
		'member_grade_id',
		'discount',
		'discount_money'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		self._init_slot_from_model(db_model)