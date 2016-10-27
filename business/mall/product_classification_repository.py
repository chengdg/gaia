# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.product_classification import ProductClassification

class ProductClassificationRepository(business_model.Service):
	def get_product_classifications(self):
		models = mall_models.Classification.select()
		return [ProductClassification(model) for model in models]

	def get_child_product_classifications(self, father_id):
		"""
		获得下一级子分类集合
		"""
		models = mall_models.Classification.select().dj_where(father_id=father_id)
		return [ProductClassification(model) for model in models]

	def delete_product_classification(self, id):
		"""
		删除指定的供货商
		"""
		mall_models.Classification.update(status=mall_models.CLASSIFICATION_OFFLINE).dj_where(id=id).execute()

	def get_children_product_classifications(self, father_id):
		"""
		获得所有子分类集合(包括子级和子级的子级)
		"""
		father_id = int(father_id)
		models = list(mall_models.Classification.select())
		children = []
		child_ids = set()

		models.sort(lambda x,y: cmp(x.father_id, y.father_id))
		for model in models:
			if (model.father_id in child_ids) or (model.id == father_id):
				children.append(model)
				child_ids.add(model.id)

		return children
