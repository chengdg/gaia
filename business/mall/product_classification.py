# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.corporation_factory import CorporationFactory


class ProductClassification(business_model.Model):
	"""
	商品分类
	"""
	__slots__ = (
		'id',
        'name',
        'status',
        'father_id',
        'level',
        'product_count',
        'note',
        'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

			if model.status == mall_models.CLASSIFICATION_ONLINE:
				self.status = 'online'
			else:
				self.status = 'offline'

	def get_father_classification(self):
		"""
		获得父级分类
		"""
		model = mall_models.Classification.select().dj_where(id=self.father_id).get()
		return ProductClassification(model)

	def update(self, name, note):
		"""
		更新商品分类
		"""
		mall_models.Classification.update(name=name, note=note).dj_where(id=self.id).execute()

	def is_used_by_product(self):
		"""
		判断该classification是否已被使用
		"""
		return mall_models.ClassificationHasProduct.select().dj_where(classification_id=self.id).count() > 0

	@staticmethod
	@param_required(['name', 'father_id', 'note'])
	def create(args):
		"""
		创建商品分类
		"""
		corp_id = CorporationFactory.get().id

		father_id = int(args['father_id'])
		if father_id == 0:
			level = 1		
		else:
			father_model = mall_models.Classification.select().dj_where(id=father_id).get()
			level = father_model.level + 1

		model = mall_models.Classification.create(
			name = args['name'],
			father_id = args['father_id'],
			note = args['note'],
			level = level
		)

		return ProductClassification(model)

