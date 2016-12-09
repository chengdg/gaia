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

	def delete_qualification_by_ids(self, ids):
		mall_models.ClassificationQualification.delete().dj_where(id__in=ids).execute()
