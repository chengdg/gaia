# -*- coding: utf-8 -*-

from db.mall import models as mall_models

from business import model as business_model
from business.mall.product_classification.product_classification import ProductClassification
from business.mall.product_classification.product_classification_qualification import ProductClassificationQualification

class ProductClassificationRepository(business_model.Service):
	def get_root_product_classifications(self):
		models = mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE, father_id=0)
		return [ProductClassification(model) for model in models]

	def get_product_classifications(self):
		"""
		获得所有子分类集合(包括子级和子级的子级)
		如果是供货商，则获取帐号配置中的分类
		"""
		if self.corp.is_supplier():
			models = mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE, id__in=self.corp.details.classification_ids)
			children = []
			for father in models:
				children += self.get_children_product_classifications(father.id)
			return children
		else:
			models = mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE).order_by(-mall_models.Classification.created_at)
			return [ProductClassification(model) for model in models]

	def get_product_classification(self, id):
		model = mall_models.Classification.select().dj_where(id=id).get()
		return ProductClassification(model)

	def get_product_classification_by_ids(self, classification_ids):
		models = mall_models.Classification.select().dj_where(id__in=classification_ids)
		return [ProductClassification(model) for model in models]

	def get_classification_by_product_id(self, product_id):
		model = mall_models.ClassificationHasProduct.select().dj_where(product_id=product_id).first()
		return ProductClassification(model.classification)

	def get_classification_by_product_ids(self, product_ids):
		models = mall_models.ClassificationHasProduct.select().dj_where(product_id__in=product_ids)
		return [ProductClassification(model.classification) for model in models]

	def check_labels(self, classifications, has_label_dict=None):
		"""
		递归检查分类是否配置了标签
		配置了标签的分类，其子分类都视为已配置标签
		:return:
		"""
		has_label_dict = has_label_dict if has_label_dict else dict()
		classification_ids = [c.id for c in classifications]
		father_ids = [c.father_id for c in classifications if c.father_id > 0]
		child_id2father_id = {c.id: c.father_id for c in classifications}
		father_has_label_dict = dict()

		if len(father_ids) > 0:
			father_classifications = mall_models.Classification.select().dj_where(id__in=father_ids)
			father_has_label_dict = self.check_labels(father_classifications, has_label_dict)

		for classification_id in classification_ids:
			has_label_dict[classification_id] = False
			if father_has_label_dict and child_id2father_id[classification_id] > 0 and father_has_label_dict[child_id2father_id[classification_id]]:
				has_label_dict[classification_id] = True

		models = mall_models.ClassificationHasLabel.select().dj_where(classification_id__in=classification_ids)
		for model in models:
			classification_id = model.classification_id
			if model.label_id:
				has_label_dict[classification_id] = True
		return has_label_dict


	def delete_product_classification(self, classification_id):
		"""
		删除指定的商品分类
		"""
		# 同时删除分类及其子分类
		mall_models.Classification.update(status=mall_models.CLASSIFICATION_OFFLINE).where((mall_models.Classification.id==classification_id) | (mall_models.Classification.father_id==classification_id)).execute()

	def get_children_product_classifications(self, father_id, with_father=True):
		"""
		获得所有子分类集合(包括子级和子级的子级)
		"""
		father_id = int(father_id)
		if self.corp.is_supplier():
			models = list(mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE)
						  .where((mall_models.Classification.id << self.corp.details.classification_ids) | (
																  mall_models.Classification.father_id << self.corp.details.classification_ids)))
		else:
			models = list(mall_models.Classification.select().dj_where(status=mall_models.CLASSIFICATION_ONLINE))
		children = []
		child_ids = set()

		models.sort(lambda x,y: cmp(x.father_id, y.father_id))
		if father_id == 0:
			return [ProductClassification(model) for model in models]

		for model in models:
			if (model.father_id in child_ids):
				children.append(ProductClassification(model))
				child_ids.add(model.id)

			if model.id == father_id:
				child_ids.add(model.id)
				if with_father:
					children.append(ProductClassification(model))

		return children

	def get_child_product_classifications(self, father_id):
		"""
		获得子分类，不包含子分类的子分类
		"""
		father_id = int(father_id)
		models = mall_models.Classification.select().dj_where(father_id=father_id, status=mall_models.CLASSIFICATION_ONLINE)

		return [ProductClassification(model) for model in models]

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

	def get_qualifications_by_classification_ids(self, classification_ids):
		models = mall_models.ClassificationQualification.select().dj_where(classification_id__in=classification_ids)
		return [ProductClassificationQualification(model) for model in models]