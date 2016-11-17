# -*- coding: utf-8 -*-
"""
买赠
"""
from business import model as business_model
from db.mall import models as mall_models
from db.mall import promotion_models
import settings


class PremiumSale(business_model.Model):
	"""
	买赠
	"""
	__slots__ = (
		'count',
		'is_enable_cycle_mode'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		if db_model:
			self._init_slot_from_model(db_model)
			self.context['premium_sale_model'] = db_model

	@property
	def premium_products(self):
		premium_sale_model = self.context['premium_sale_model']
		promotion = promotion_models.Promotion.select().dj_where(detail_id=premium_sale_model.id).get()
		product2promotion = promotion_models.ProductHasPromotion.get(promotion=promotion.id)
		main_product = product2promotion.product

		premium_sale_products = promotion_models.PremiumSaleProduct.select().dj_where(premium_sale_id=premium_sale_model.id)
		product_ids = [premium_sale_product.product_id for premium_sale_product in premium_sale_products]

		products = mall_models.Product.select().dj_where(id__in=product_ids)

		pool_product_list = [p.product_id for p in mall_models.ProductPool.select().dj_where(
			woid=premium_sale_model.owner_id,
			status=mall_models.PP_STATUS_ON)]

		id2product = dict([(product.id, product) for product in products])
		premium_products = []
		for premium_sale_product in premium_sale_products:
			product_id = premium_sale_product.product_id
			product = id2product[product_id]

			if pool_product_list and product_id in pool_product_list:
				shelve_type = mall_models.PRODUCT_SHELVE_TYPE_ON
			else:
				shelve_type = product.shelve_type

			data = {
				'id': product.id,
				'name': product.name,
				'thumbnails_url': '%s%s' % (settings.IMAGE_HOST, product.thumbnails_url) if product.thumbnails_url.find(
					'http') == -1 else product.thumbnails_url,
				'original_premium_count': premium_sale_product.count,
				'premium_count': premium_sale_product.count,
				'premium_unit': premium_sale_product.unit,
				'premium_product_id': premium_sale_product.product_id,
				'supplier': main_product.supplier,
				'shelve_type': shelve_type,
				'is_deleted': product.is_deleted
			}
			premium_products.append(data)
		return premium_products