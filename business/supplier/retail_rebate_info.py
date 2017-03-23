# -*- coding: utf-8 -*-

from business import model as business_model

class RetailRebateInfo(business_model.Model):
	"""
	零售返点模式的信息
	"""
	__slots__ = (
		'id',
		'rebate'
	)

	def __init__(self, rebate):
		business_model.Model.__init__(self)

		if type != None:
			self.rebate = rebate