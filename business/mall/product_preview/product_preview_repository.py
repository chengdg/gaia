# -*- coding: utf-8 -*-
from business import model as business_model
from business.mall.corporation_factory import CorporationFactory

from db.mall import models as mall_models
from product import ProductPreview


class ProductPreviewRepositroy(business_model.Service):
	def get_products(self):
		models = mall_models.ProductPreview.select().dj_where(owner_id=self.corp.id)
		return [ProductPreview(model) for model in models]