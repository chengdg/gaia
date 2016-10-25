# -*- coding: utf-8 -*-
from business import model as business_model

class ProductLabel(business_model.Model):
	"""
	商品标签
	"""
	__slots__ = (
		'id',
		'name',
		'label_group_id',
		'owner_id',
		'created_at',
		'is_deleted'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)