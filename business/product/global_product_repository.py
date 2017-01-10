# -*- coding: utf-8 -*-

from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models

class GlobalProductRepository(business_model.Service):

	def get_products_by_ids(self, product_ids, fill_options=None):
		"""
		根据商品id获得商品集合
		@param product_ids: 商品id集合
		"""
		fill_options = fill_options if fill_options else {}
		product_models = mall_models.Product.select().dj_where(id__in=product_ids)
		products = [Product(model) for model in product_models]
		from business.product.fill_product_detail_service import FillProductDetailService
		fill_product_detail_service = FillProductDetailService.get(None)
		fill_product_detail_service.fill_detail(products, fill_options)

		pool_products = mall_models.ProductPool.select().dj_where(product_id__in=product_ids)
		id2product = dict([(product.id, product) for product in products])
		for pool_product in pool_products:
			product = id2product[pool_product.product_id]
			if pool_product.type == mall_models.PP_TYPE_SYNC:
				product.create_type = 'sync'
				product.sync_at = pool_product.sync_at
			else:
				product.create_type = 'create'

		#按照product_ids中id的顺序对products进行顺序调整
		result = []
		for product_id in product_ids:
			product_id = int(product_id)
			result.append(id2product[product_id])
		return result