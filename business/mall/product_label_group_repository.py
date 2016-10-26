# -*- coding: utf-8 -*-
from business import model as business_model
from db.mall import models as mall_models
from business.mall.product_label_group import ProductLabelGroup


class ProductLabelGroupRepositroy(business_model.Service):
	def get_label_groups(self):
		models = mall_models.ProductLabelGroup.select().dj_where(owner_id=self.corp.id)
		product_label_groups = [ProductLabelGroup(model) for model in models]
		return product_label_groups