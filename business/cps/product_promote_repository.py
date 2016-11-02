# -*- coding: utf-8 -*-

import json

from business import model as business_model
from eaglet.core import paginator

from db.mall import models as mall_models
from business.cps.product_promote import ProductPromote
from business.product.product import Product
from business.product.fill_product_detail_service import FillProductDetailService


class ProductPromoteRepository(business_model.Service):

	def get_product_promote(self, promote_id):

		promote = mall_models.PromoteDetail.get(id=promote_id)
		return ProductPromote.from_model({'db_model': promote})

	def get_product_pool_promotes(self, target_page, filters):
		filters['promote_status'] = mall_models.PROMOTING
		filters['__f-status-equal'] = mall_models.PP_STATUS_OFF
		return self.search_promotes(filters=filters, target_page=target_page)

	def search_promotes(self, filters, target_page):

		promote_models = mall_models.PromoteDetail.select().dj_where(promote_status=filters.pop('promote_status'))
		fill_options = {
			'with_category': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_shelve_status': True,
			'with_supplier_info': True,
			'with_classification': True,
			'with_sales': True
		}
		product_pool = self.corp.product_pool

		options = {
			'order_by_display_index': False
		}
		# target_page.count_per_page = 1000000
		product_ids = [promote.product_id for promote in promote_models]
		filters['__f-product_id-in'] = json.dumps(product_ids)
		products, pageinfo = product_pool.get_products(target_page, fill_options, options, filters)

		promotes = self.__fill_promotes(promote_models, products)

		return promotes, pageinfo

	def __fill_promotes(self, promote_models, products):
		promotes = []
		for product in products:
			promote_model = filter(lambda k: k.id, promote_models)[0]
			promote = ProductPromote.from_model({'db_model': promote_model})
			promote.product = product

			promotes.append(promote)
		return promotes
