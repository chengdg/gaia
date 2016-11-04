# -*- coding: utf-8 -*-
"""
积分应用
"""
from business.mall.promotion import promotion


class IntegralSale(promotion.Promotion):
	"""
	积分应用
	"""
	__slots__ = (
		'integral_sale_type',
		'display_integral_sale_type',
		'is_permanant_active',
		'rules',
		'discount',
		'discount_money'
	)

	def __init__(self, promotion_model=None):
		promotion.Promotion.__init__(self)
		self.type_name = 'integral_sale'
		if promotion_model:
			self._init_promotion_slot_from_model(promotion_model)