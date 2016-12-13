# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.corporation_factory import CorporationFactory
from business.mall.classification.product_classification_qualification import ProductClassificationQualification


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

	def get_qualifications(self):
		models = mall_models.ClassificationQualification.select().dj_where(classification_id=self.id)
		return [ProductClassificationQualification(model) for model in models]

	def get_qualification(self, id):
		model = mall_models.ClassificationQualification.select().dj_where(id=id).get()
		return ProductClassificationQualification(model)

	def add_qualification(self, name):
		"""
		创建商品分组特殊资质
		"""
		model = mall_models.ClassificationQualification.create(
			classification = self.id,
			name = name
		)
		return ProductClassificationQualification(model)

	def update_qualification(self, qualification_id, name):
		"""
		修改商品分组特殊资质
		"""
		mall_models.ClassificationQualification.update(name=name).dj_where(id=qualification_id).execute()
	
	def delete_qualification_by_ids(self, qualification_ids):
		"""
		删除商品分组特殊资质
		"""
		mall_models.ClassificationQualification.delete().dj_where(id__in=qualification_ids).execute()

	def set_qualifications(self, qualification_infos):
		"""
		设置商品分组特殊资质
		"""
		old_ids = [int(qualification.id) for qualification in self.get_qualifications()]
		need_keep_ids = []
		need_remove_ids = []

		#循环本次需要的资质集合，得到编辑后被删除的特殊资质id
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				#组织需要保留的id集合
				need_keep_ids.append(qualification_info['id'])
				#更新资质
				self.update_qualification(qualification_info['id'], qualification_info['name'])
			else:
				#新增资质
				self.add_qualification(qualification_info['name'])
		for old_id in old_ids:
			if old_id not in need_keep_ids:
				need_remove_ids.append(old_id)
		
		self.delete_qualification_by_ids(need_remove_ids)		
		
		return {}