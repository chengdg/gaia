# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from business import model as business_model
from business.mall.product_label.product_label import ProductLabel
from business.mall.product_classification.product_classification_repository import ProductClassificationRepository


class ProductLabelRepository(business_model.Service):
	def get_labels_by_classification_id(self, classification_id):
		relations = mall_models.ClassificationHasLabel.select().dj_where(classification_id=classification_id)
		label_ids = [r.label_id for r in relations]
		return self.get_labels(label_ids)

	def get_labels_by_group_ids(self, label_group_ids):
		db_models = mall_models.ProductLabel.select().dj_where(label_group_id__in=label_group_ids, is_deleted=False)
		return [ProductLabel(model) for model in db_models]

	def get_labels(self, label_ids=None):
		if label_ids != None:
			db_models = mall_models.ProductLabel.select().dj_where(id__in=label_ids, is_deleted=False)
		else:
			db_models = mall_models.ProductLabel.select().dj_where(is_deleted=False)
		return [ProductLabel(model) for model in db_models]

	def get_label_product_relations(self, product_ids):
		"""
		返回商品id对标签ids的映射
		:return: [{
			product_id: [lable1, label2]
		}]
		"""
		label_id2model = {l.id: l for l in mall_models.ProductLabel.select().dj_where(is_deleted=False)}
		p2c_relations = dict()
		classification_ids = []
		for ch in mall_models.ClassificationHasProduct.select().dj_where(product_id__in=product_ids):
			p2c_relations[ch.product_id] = ch.classification_id
			classification_ids.append(ch.classification_id)
		c2ls_relations = dict()
		for cl in mall_models.ClassificationHasLabel.select().dj_where(classification_id__in=classification_ids):
			label = label_id2model[cl.label_id]
			if not c2ls_relations.has_key(cl.classification_id):
				c2ls_relations[cl.classification_id] = [label]
			else:
				c2ls_relations[cl.classification_id].append(label)

		product_has_labels = mall_models.ProductHasLabel.select().dj_where(product_id__in=product_ids)
		product_id2labels = dict()
		for product_has_label in product_has_labels:
			product_id = product_has_label.product_id
			label_id = product_has_label.label_id
			label = label_id2model.get(label_id)
			if not label:
				continue
			if not product_id2labels.has_key(product_id):
				product_id2labels[product_id] = [label]
			else:
				product_id2labels[product_id].append(label)

		p2ls = dict()
		for product_id in product_ids:
			if product_id2labels.get(product_id) and len(product_id2labels[product_id]) > 0:
				p2ls[product_id] = product_id2labels[product_id]
			else:
				classification_id = p2c_relations.get(product_id)
				if not classification_id:
					continue
				labels = c2ls_relations.get(classification_id, [])
				p2ls[product_id] = labels

		return p2ls

	def delete_labels(self, label_ids):
		mall_models.ProductLabel.update(is_deleted=True).dj_where(id__in=label_ids).execute()
		# 更新已选择这些被删除标签的商品的信息
		mall_models.ProductHasLabel.delete().dj_where(label_id__in=label_ids).execute()
		# 更新已选择这些被删除标签的商品分类的信息
		mall_models.ClassificationHasLabel.delete().dj_where(label_id__in=label_ids).execute()