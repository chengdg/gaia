# -*- coding: utf-8 -*-
"""
买赠
"""
from business.mall.promotion import promotion


class PremiumSale(promotion.Promotion):
	"""
	买赠
	"""
	__slots__ = (
		'count',
		'is_enable_cycle_mode',
		'premium_products'
	)

	def __init__(self, promotion_model=None):
		promotion.Promotion.__init__(self)

		if promotion_model:
			self._init_promotion_slot_from_model(promotion_model)

		self.type_name = 'premium_sale'