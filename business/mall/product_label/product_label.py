# -*- coding: utf-8 -*-

from business import model as business_model

class ProductLabel(business_model.Model):
	"""
	商品标签
	"""
	__slots__ = (
		'id',
		'label_group_id',
		'name',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)