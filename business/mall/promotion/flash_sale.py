# -*- coding: utf-8 -*-
"""
限时抢购
"""
from business import model as business_model


class FlashSale(business_model.Model):
	"""
	限时抢购
	"""
	__slots__ = (
		'limit_period',
		'promotion_price',
		'count_per_purchase',
		'count_per_period'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		if db_model:
			self._init_slot_from_model(db_model)