# -*- coding: utf-8 -*-

from business.mall.corporation_factory import CorporationFactory
from business import model as business_model
from business.mall.product_label.product_label import ProductLabel
from db.mall import models as mall_models

class ProductLabelGroup(business_model.Model):
	"""
	商品标签
	"""
	__slots__ = (
		'id',
		'name',
		'is_deleted',
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

	@staticmethod
	def create(label_group_name):
		"""
		创建商品标签分组
		"""
		corp_id = CorporationFactory.get().id
		#检查重名
		exist_group_models = mall_models.ProductLabelGroup.select().dj_where(name=label_group_name, owner_id=corp_id, is_deleted=False)
		if exist_group_models.count() > 0:
			return u'商品标签分类已存在'

		model = mall_models.ProductLabelGroup.create(
			owner_id = corp_id,
			name = label_group_name
		)
		return ProductLabelGroup(model)

	def add_label(self, label_name):
		"""
		添加标签
		"""
		if mall_models.ProductLabel.select().dj_where(name=label_name, is_deleted=False).count() > 0:
			return u'创建失败，请检查是否重名'

		new_model = mall_models.ProductLabel.create(
			label_group_id = self.id,
			owner_id = CorporationFactory.get().id,
			name = label_name
		)
		return ProductLabel(new_model)
