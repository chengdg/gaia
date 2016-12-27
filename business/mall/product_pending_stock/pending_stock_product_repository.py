# -*- coding: utf-8 -*-
import json

from eaglet.core import paginator

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from business.product.product_factory import ProductFactory

from db.mall import models as mall_models
from pending_stock_product import PendingProduct


class PendingStockProductRepository(business_model.Service):
	def filter_products(self, query_dict, page_info):
		query = {
			'is_deleted': False
		}
		if query_dict.get('customer_name'):
			pass
		if self.corp.is_weizoom_corp:
			query['review_status'] = mall_models.PENDING_PRODUCT_STATUS['SUBMIT']
		else:
			query['owner_id'] = self.corp.id
		db_models = mall_models.ProductPendingStock.select().dj_where(**query)

		pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)

		return pageinfo, [PendingProduct(model) for model in db_models]

	def review_accept(self, product_ids):
		"""
		商品审核通过
		:param product_ids: 商品id列表，可批量审核
		"""
		mall_models.ProductPendingStock.update(
			review_status = mall_models.PENDING_PRODUCT_STATUS['ACCEPT'],
			is_updated = False
		).dj_where(id__in=product_ids).execute()

		#入库商品
		product_factory = ProductFactory.get(CorporationFactory.get())
		for product_id in product_ids:
			pending_product = PendingProduct.get(product_id)
			base_info = {
				'name': pending_product.name,
				'promotion_title': pending_product.promotion_title,
				'supplier_id': pending_product.owner_id,
				'detail': pending_product.remark,
				'purchase_price': str(pending_product.settlement_price),
				'min_limit': 0,
				'is_member_product': False,
				'is_enable_bill': False
			}

			image_info = {
				'images': []
			}
			properties = []
			categories = []

			logistics_info = {
				'postage_type': 'unified_postage_type' if pending_product.has_same_postage else 'custom_postage_type',
				'postage_id': pending_product.postage_id,
				'unified_postage_money': str(pending_product.postage_money),
				'limit_zone_type': pending_product.limit_zone_type,
				'limit_zone_id': pending_product.limit_zone
			}

			pay_info = {
				'is_use_online_pay_interface': True,
				'is_use_cod_pay_interface': False
			}

			models_info = {
				'standard_model': {
					'price': str(pending_product.price),
					'purchase_price': str(pending_product.settlement_price),
					'weight': pending_product.weight,
					'stock_type': 'limit',
					'stocks': pending_product.store,
					'user_code': ''
				},
				'custom_models': []
			}

			product_factory.create_product({
				'base_info': base_info,
				'image_info': image_info,
				'logistics_info': logistics_info,
				'pay_info': pay_info,
				'properties': properties,
				'categories': categories,
				'models_info': models_info
			})

	def review_reject(self, product_id, reason):
		"""
		审核不通过(入库审核，修改审核)
		"""
		pass