# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from business.mall.product_classification.product_classification_label import ProductClassificationLabel
from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.corporation_factory import CorporationFactory
from business.mall.product_classification.product_classification_qualification import ProductClassificationQualification


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
			owner_id = CorporationFactory.get().id,
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

	def set_labels(self, selected_labels):
		"""
		设置商品分类标签
		:return:
		"""
		#首先删除已有的标签
		self.delete_labels()
		bulk_create = []
		if len(selected_labels) > 0:
			for label_id in selected_labels:
				bulk_create.append(dict(
					classification = self.id,
					label_id = label_id
				))
			ProductClassificationLabel.create_many(bulk_create)

	def delete_labels(self):
		"""
		删除所有标签
		:return:
		"""
		mall_models.ClassificationHasLabel.delete().dj_where(classification_id=self.id).execute()

	def get_labels(self, classification_ids=None):
		"""
		获取分类的标签
		"""
		classification_ids = classification_ids if classification_ids else []
		classification_ids.append(self.id)
		#首先检查父分类
		if self.father_id > 0:
			corp = CorporationFactory.get()
			father_model = corp.product_classification_repository.get_product_classification(self.father_id)
			father_model.get_labels(classification_ids)
		models = mall_models.ClassificationHasLabel.select().dj_where(classification_id__in=classification_ids)
		return [ProductClassificationLabel(model) for model in models]

	def get_label_group_relation(self):
		"""
		:return:

		[{
			'label_group_id': label_group_A,
			'label_ids': [label_a1, label_a2, label_a3]
		},{
			'label_group_id': label_group_B,
			'label_ids': [label_b1, label_b2, label_b3]
		}]
		"""
		classification_labels = self.get_labels()
		all_label_ids = []
		label_id2classifi = dict()
		for model in classification_labels:
			label_id = model.label_id
			all_label_ids.append(label_id)
			label_id2classifi[label_id] = model.classification_id

		corp = CorporationFactory.get()
		labels = corp.product_label_repository.get_labels(all_label_ids)
		label_id2group_id = {db_model.id: db_model.label_group_id for db_model in mall_models.ProductLabel.select().dj_where(id__in=all_label_ids, is_deleted=False)}

		label_group_has_label = dict()
		classification_has_own_label = dict()
		for label in labels:
			label_id = label.id
			label_group_id = label_id2group_id[label_id]
			if not label_group_has_label.has_key(label_group_id):
				label_group_has_label[label_group_id] = [label_id]
			else:
				label_group_has_label[label_group_id].append(label_id)

			classification_has_own_label[label_id] = True if label_id2classifi[label_id] == self.id else False

		relations = []
		for label_group_id, label_ids in label_group_has_label.items():
			relations.append({
				'label_group_id': label_group_id,
				'label_ids': list(set(label_ids))  # 去重
			})

		return {
			'relations': relations,
			'classification_has_own_label': classification_has_own_label
		}

	def add_product(self, product_id):
		"""
		增加分类下的商品
		"""
		mall_models.Classification.update(product_count=mall_models.Classification.product_count+1).dj_where(id=self.id).execute()
		#建立关系
		mall_models.ClassificationHasProduct.create(
			classification = self.id,
			product_id = product_id,
			woid = CorporationFactory.get().id
		)

	@property
	def total_product_count(self):
		"""
		上级分类的商品数等于所有下级分类商品数的总和
		"""
		curr_classification_ids = [self.id]
		product_count = self.product_count
		while len(curr_classification_ids) > 0:
			childs = mall_models.Classification.select().dj_where(father_id__in=curr_classification_ids)
			curr_classification_ids = []
			if childs.count() > 0:
				for child in childs:
					product_count += child.product_count
					curr_classification_ids.append(child.id)

		return product_count