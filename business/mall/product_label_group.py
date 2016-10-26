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
		'owner_id',
		'labels',
		'created_at',
		'is_deleted'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.labels = self.__fill_labels()

	def __fill_labels(self):
		label_models = mall_models.ProductLabel.select().dj_where(label_group_id=self.id, is_deleted=False, owner_id=self.owner_id)
		labels = []
		for model in label_models:
			labels.append({
				'label_id': model.id,
				'label_name': model.name
			})
		return labels