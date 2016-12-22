# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from business import model as business_model
from business.mall.product_label.product_label import ProductLabel


class ProductLabelRepository(business_model.Service):
	def get_product_labels(self, product_id):
		relation_models = mall_models.ProductHasLabel.select().dj_where(id=product_id)
		label_ids = [relation.label_id for relation in relation_models]
		models = mall_models.ProductLabel.select().dj_where(id__in=label_ids, is_deleted=False)
		return [ProductLabel(model) for model in models]

	def get_labels(self, label_ids):
		models = mall_models.ProductLabel.select().dj_where(id__in=label_ids, is_deleted=False)
		return [ProductLabel(model) for model in models]

	def delete_labels(self, label_ids):
		mall_models.ProductLabel.update(is_deleted=True).dj_where(id__in=label_ids).execute()
		# 更新已选择这些被删除标签的商品的信息
		mall_models.ProductHasLabel.delete().dj_where(label_id__in=label_ids).execute()
		# 更新已选择这些被删除标签的商品分类的信息
		mall_models.ClassificationHasLabel.delete().dj_where(label_id__in=label_ids).execute()