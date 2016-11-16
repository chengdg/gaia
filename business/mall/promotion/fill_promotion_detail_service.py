# -*- coding: utf-8 -*-

from business import model as busniess_model
from business.mall.promotion.integral_sale import IntegralSale
from db.mall import promotion_models
from db.mall import models as mall_models
import settings


class FillPromotionDetailService(busniess_model.Service):
	"""
	对促销集合批量填充详情服务
	"""
	def __fill_flash_sale_details(self, promotions):
		"""
		填充限时抢购的详细信息
		"""
		flash_sale_ids = []
		detail_id2promotion = {}
		for promotion in promotions:
			flash_sale_ids.append(promotion.context['detail_id'])
			detail_id2promotion[promotion.context['detail_id']] = promotion
		flash_sale_models = promotion_models.FlashSale.select().dj_where(id__in=flash_sale_ids)
		for model in flash_sale_models:
			flash_sale_detail = {
				'count_per_period': model.count_per_period,
				'limit_period': model.limit_period,
				'count_per_purchase': model.count_per_purchase,
				'promotion_price': model.promotion_price
			}
			detail_id2promotion[model.id].detail = flash_sale_detail

	def __fill_integral_sale_rule_details(self, promotions):
		"""
		填充与积分应用相关的`积分应用规则`
		"""
		integral_sale_ids = []
		detail_id2promotion = {}
		for promotion in promotions:
			integral_sale_detail_id = promotion.context['detail_id']
			integral_sale_ids.append(integral_sale_detail_id)
			detail_id2promotion[integral_sale_detail_id] = promotion

		integral_sale_models = promotion_models.IntegralSale.select().dj_where(id__in=integral_sale_ids)
		integral_sale_id2integral_sale_rules = dict([(model.integral_sale_id, model) for model in promotion_models.IntegralSaleRule.select().dj_where(integral_sale_id__in=integral_sale_ids)])
		for model in integral_sale_models:
			integral_sale = IntegralSale(model)
			integral_sale_id = model.id
			integral_sale.add_rule(integral_sale_id2integral_sale_rules[integral_sale_id])
			integral_sale.calculate_discount()
			integral_sale_rule_detail = {
				'rules': integral_sale.rules,
				'discount': integral_sale.discount,
				'discount_money': integral_sale.discount_money,
				'is_permanant_active': integral_sale.is_permanant_active
			}
			detail_id2promotion[integral_sale_id].detail = integral_sale_rule_detail

	def __fill_premium_products_details(self, promotions, corp):
		"""
		填充与限时抢购相关的`促销商品详情`
		"""
		premium_sale_ids = []
		detail_id2promotion = {}
		for promotion in promotions:
			prenium_sale_detail_id = promotion.context['detail_id']
			premium_sale_ids.append(prenium_sale_detail_id)
			detail_id2promotion[prenium_sale_detail_id] = promotion

		premium_sale_models = promotion_models.PremiumSale.select().dj_where(id__in=premium_sale_ids)
		for model in premium_sale_models:
			detail_id2promotion[model.id].detail = {
				'count': model.count,
				'is_enable_cycle_mode': model.is_enable_cycle_mode,
				'premium_products': []
			}

		premium_sale_products = promotion_models.PremiumSaleProduct.select().dj_where(
				owner_id=corp.id,
				premium_sale_id__in=premium_sale_ids)
		product_ids = [premium_sale_product.product_id for premium_sale_product in premium_sale_products]

		products = mall_models.Product.select().dj_where(id__in=product_ids)

		pool_product_list = [p.product_id for p in mall_models.ProductPool.select().dj_where(
			woid=corp.id,
			status=mall_models.PP_STATUS_ON)]

		id2product = dict([(product.id, product) for product in products])

		for premium_sale_product in premium_sale_products:
			premium_sale_id = premium_sale_product.premium_sale_id
			promotion_id = detail_id2promotion[premium_sale_id].id

			product2promotion = promotion_models.ProductHasPromotion.get(promotion=promotion_id)
			main_product = product2promotion.product

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
			detail_id2promotion[premium_sale_id].detail['premium_products'].append(data)

	def fill_detail(self, promotions, corp):
		"""
		为促销填充促销特定数据
		"""
		type2promotions = dict()
		for promotion in promotions:
			type2promotions.setdefault(promotion.type, []).append(promotion)
		for promotion_type, promotions in type2promotions.items():
			if promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
				self.__fill_flash_sale_details(promotions)
			elif promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
				self.__fill_premium_products_details(promotions, corp)
			elif promotion_type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
				self.__fill_integral_sale_rule_details(promotions)
