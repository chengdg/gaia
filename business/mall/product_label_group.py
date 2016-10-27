# -*- coding: utf-8 -*-
from business import model as business_model
from business.mall.product_label import ProductLabel
from db.mall import models as mall_models

class ProductLabelGroup(business_model.Model):
	"""
	商品标签
	"""
	__slots__ = (
		'id',
		'name',
		'labels',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)

	def get_labels(self):
		label_models = mall_models.ProductLabel.select().dj_where(label_group_id=self.id, is_deleted=False)
		labels = []
		for model in label_models:
			labels.append(ProductLabel(model))
		return labels