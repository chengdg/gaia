# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.product_classification_qualification import ProductClassificationQualification

class ProductClassificationQualificationRepository(business_model.Service):
	def get_product_classification_qualifications(self, classification_id):
		models = mall_models.ClassificationQualification.select().dj_where(classification_id=classification_id)
		return [ProductClassificationQualification(model) for model in models]

	def get_product_classification_qualification(self, id):
		model = mall_models.ClassificationQualification.select().dj_where(id=id).get()
		return ProductClassificationQualification(model)

	def delete_qualification_by_ids(self, ids):
		mall_models.ClassificationQualification.delete().dj_where(id__in=ids).execute()

	@staticmethod
	@param_required(['classification_id', 'qualification_infos'])
	def update_qualifications(args):
		"""
		修改商品分组特殊资质
		"""
		qualification_infos = args['qualification_infos']
		classification_id = int(args['classification_id'])
		classification_qualification_repository = ProductClassificationQualificationRepository()
		old_ids = [int(classification.id) for classification in classification_qualification_repository.get_product_classification_qualifications(classification_id)]
		need_keep_ids = []
		need_remove_ids = []

		#循环本次需要的资质集合，得到编辑后被删除的特殊资质id
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				#组织需要保留的id集合
				need_keep_ids.append(qualification_info['id'])
				#更新资质
				product_classification_qualification = classification_qualification_repository.get_product_classification_qualification(qualification_info['id'])
				product_classification_qualification.update(qualification_info['name'])
			else:
				#新增资质
				ProductClassificationQualification.create(classification_id, qualification_info['name'])
		for old_id in old_ids:
			if old_id not in need_keep_ids:
				need_remove_ids.append(old_id)
		
		classification_qualification_repository.delete_qualification_by_ids(need_remove_ids)		
		
		return {}
