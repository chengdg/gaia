# -*- coding: utf-8 -*-
from business import model as business_model
from business.mall.corporation_factory import CorporationFactory

from db.mall import models as mall_models
from pending_product import PendingProduct


class PendingProductRepository(business_model.Service):
	def filter_products(self, query_dict):
		query = {
			'is_deleted': False
		}
		if query_dict.get('customer_name'):
			pass
		if self.corp.is_weizoom_corp:
			query['review_status'] = mall_models.PENDING_PRODUCT_STATUS['SUBMIT']
		else:
			query['owner_id'] = self.corp.id
		models = mall_models.ProductPendingStock.select().dj_where(**query)
		return [PendingProduct(model) for model in models]

	def get_pending_product(self, product_id):
		model = mall_models.ProductPendingStock.select().dj_where(id=product_id).get()
		return PendingProduct(model)