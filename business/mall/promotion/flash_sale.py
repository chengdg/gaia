# -*- coding: utf-8 -*-
"""
限时抢购
"""
from business.mall.promotion import promotion


class FlashSale(promotion.Promotion):
	"""
	限时抢购
	"""
	__slots__ = (
		'limit_period',
		'promotion_price',
		'count_per_purchase',
		'count_per_period'
	)

	def __init__(self, promotion_model=None):
		promotion.Promotion.__init__(self)
		self.type_name = 'flash_sale'

		if promotion_model:
			self._init_promotion_slot_from_model(promotion_model)

	def _get_detail_data(self):
		return {
			'limit_period': self.limit_period,
			'promotion_price': self.promotion_price,
			'count_per_purchase': self.count_per_purchase,
			'count_per_period': self.count_per_period
		}