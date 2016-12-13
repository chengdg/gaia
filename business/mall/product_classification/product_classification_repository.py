# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.product_classification.product_classification import ProductClassification

class ProductClassificationRepository(business_model.Service):
	def get_product_classifications(self):
		models = mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE)
		return [ProductClassification(model) for model in models]

	def get_product_classification(self, id):
		model = mall_models.Classification.select().dj_where(id=id).get()
		return ProductClassification(model)

	def get_child_product_classifications(self, father_id):
		"""
		获得下一级子分类集合
		"""
		models = mall_models.Classification.select().dj_where(father_id=father_id)\
			.dj_where(status=mall_models.CLASSIFICATION_ONLINE)
		return [ProductClassification(model) for model in models]

	def delete_product_classification(self, id):
		"""
		删除指定的商品分类
		"""
		# 同时删除分类及其子分类
		mall_models.Classification.update(status=mall_models.CLASSIFICATION_OFFLINE).dj_where(id=id).dj_where(father_id=id).execute()

	def get_children_product_classifications(self, father_id):
		"""
		获得所有子分类集合(包括子级和子级的子级)
		"""
		father_id = int(father_id)
		models = list(mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE))
		children = []
		child_ids = set()

		models.sort(lambda x,y: cmp(x.father_id, y.father_id))
		for model in models:
			if (model.father_id in child_ids) or (model.id == father_id):
				children.append(model)
				child_ids.add(model.id)

		return children

	def get_product_classification_tree_by_end(self, end_id):
		"""
		获得以end_id为终结节点的classification路径的集合
		"""
		classification_id = end_id

		classifications = []
		while True:
			if classification_id == 0:
				break

			model = mall_models.Classification.select().dj_where(id=classification_id).get()
			classifications.append(ProductClassification(model))

			classification_id = model.father_id

		classifications.reverse()
		return classifications

	


	