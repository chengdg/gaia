# -*- coding: utf-8 -*-

from business import model as business_model


class ProductClassificationLabel(business_model.Model):
	"""
	商品分类标签
	"""
	__slots__ = (
		'id',
		'classification_id',
		'label_group_id',
		'label_id',
		'created_at',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)


