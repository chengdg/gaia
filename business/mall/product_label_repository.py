# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from business import model as business_model
from business.mall.product_label import ProductLabel

class ProductLabelRepository(business_model.Service):
	def get_product_labels(self, product_id):
		relation_models = mall_models.ProductHasLabel.select().dj_where(id=product_id)
		label_ids = [relation.label_id for relation in relation_models]
		models = mall_models.ProductLabel.select().dj_where(id__in=label_ids, is_deleted=False)
		return [ProductLabel(model) for model in models]

	def get_labels(self, label_ids):
		models = mall_models.ProductLabel.select().dj_where(id__in=label_ids, is_deleted=False)
		return [ProductLabel(model) for model in models]