# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy
from bdem import msgutil

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator

from business.product.product import Product
from business.mall.corporation_factory import CorporationFactory
from business.mall.category.category_product_repository import CategoryProductRepository
from gaia_conf import TOPIC


class ProductClassificationQualification(business_model.Model):
	"""
	商品分组特殊资质
	"""
	__slots__ = (
		'id',
		'classification_id',
		'name',
		'created_at',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		product_classification_qualification = ProductClassificationQualification(model)
		return product_classification_qualification

	@staticmethod
	@param_required(['classification_id', 'qualification_infos'])
	def update(args):
		"""
		修改商品分组特殊资质
		"""
		qualification_infos = args['qualification_infos']
		classification_id = int(args['classification_id'])
		classification_qualification_repository = ProductClassificationQualificationRepository()
		old_ids = [int(classification.id) for classification in classification_qualification_repository.get_product_classification_qualifications(classification_id)]
		new_ids = []
		need_del_ids = []

		#循环第一次，得到编辑后被删除的特殊资质id
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				new_ids.append(qualification_info['id'])
		for old_id in old_ids:
			if old_id not in new_ids:
				need_del_ids.append(old_id)
		
		classification_qualification_repository.delete_qualification_by_ids(need_del_ids)
		
		# 循环第二次，更新需要修改的特殊资质信息
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				#更新资质
				mall_models.ClassificationQualification.update(name=qualification_info['name']).dj_where(id=qualification_info['id']).execute()
			else:
				#新增资质
				mall_models.ClassificationQualification.create(
					classification = classification_id,
					name = qualification_info['name']
				)
		
		return {}