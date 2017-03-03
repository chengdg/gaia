# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from business import model as business_model
from business.mall.product_label.product_label import ProductLabel
from business.mall.product_classification.product_classification_repository import ProductClassificationRepository


class ProductLabelRepository(business_model.Service):
	def get_labels_by_product_id(self, product_id):
		return self.get_labels_by_product_ids([product_id])[0]

	def get_labels_by_product_ids(self, product_ids):
		classifications = ProductClassificationRepository.get().get_classification_by_product_ids(product_ids)
		return self.get_labels_by_classification_ids([c.id for c in classifications])

	def get_labels_by_classification_ids(self, classification_ids):
		relations = mall_models.ClassificationHasLabel.select().dj_where(classification__in=classification_ids)
		label_ids = [r.label_id for r in relations]
		return self.get_labels(label_ids)

	def get_labels(self, label_ids):
		db_models = mall_models.ProductLabel.select().dj_where(id__in=label_ids, is_deleted=False)
		return [ProductLabel(model) for model in db_models]

	def delete_labels(self, label_ids):
		mall_models.ProductLabel.update(is_deleted=True).dj_where(id__in=label_ids).execute()
		# 更新已选择这些被删除标签的商品的信息
		mall_models.ProductHasLabel.delete().dj_where(label_id__in=label_ids).execute()
		# 更新已选择这些被删除标签的商品分类的信息
		mall_models.ClassificationHasLabel.delete().dj_where(label_id__in=label_ids).execute()