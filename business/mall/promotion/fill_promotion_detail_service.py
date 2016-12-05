# -*- coding: utf-8 -*-

from business import model as busniess_model
from business.mall.promotion.promotion import Promotion
from business.mall.promotion.integral_sale import IntegralSale
from business.mall.promotion.flash_sale import FlashSale
from business.mall.promotion.premium_sale import PremiumSale
from db.mall import promotion_models


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
			flash_sale = FlashSale(model)
			detail_id2promotion[model.id].detail = flash_sale

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
			detail_id2promotion[integral_sale_id].detail = integral_sale

	def __fill_premium_sale_details(self, promotions, corp):
		"""
		填充与买赠相关的`促销商品详情`
		"""
		premium_sale_ids = []
		detail_id2promotion = {}
		for promotion in promotions:
			premium_sale_detail_id = promotion.context['detail_id']
			premium_sale_ids.append(premium_sale_detail_id)
			detail_id2promotion[premium_sale_detail_id] = promotion

		premium_sale_models = promotion_models.PremiumSale.select().dj_where(id__in=premium_sale_ids)
		for model in premium_sale_models:
			detail_id2promotion[model.id].detail = PremiumSale(model)

	def __fill_promotion_product_detail(self):
		"""
		填充促销相关的商品信息
		"""
		pass

	def fill_detail(self, promotions, corp, fill_options):
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
				self.__fill_premium_sale_details(promotions, corp)
			elif promotion_type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
				self.__fill_integral_sale_rule_details(promotions)

	def fill_detail_for_products(self, corp, products):
		"""
		为商品添加促销详细信息
		"""
		id2product = dict([(product.id, product) for product in products])
		product_ids = id2product.keys()

		relations = promotion_models.ProductHasPromotion.select().dj_where(product_id__in=product_ids)
		promotion_id2product_id = dict([(relation.promotion_id, relation.product_id) for relation in relations])
		promotion_ids = promotion_id2product_id.keys()

		promotion_db_models = promotion_models.Promotion.select().dj_where(id__in=promotion_ids).where(
			promotion_models.Promotion.type != promotion_models.PROMOTION_TYPE_COUPON)
		promotions = []
		for promotion_db_model in promotion_db_models:
			if (promotion_db_model.status != promotion_models.PROMOTION_STATUS_STARTED) and (
				promotion_db_model.status != promotion_models.PROMOTION_STATUS_NOT_START):
				# 跳过已结束、已删除的促销活动
				continue

			if promotion_db_model.owner_id != int(corp.id):
				continue

			promotion = Promotion(promotion_db_model)
			promotions.append(promotion)
		self.fill_detail(promotions, corp)
		# 为所有的product设置product.promotion
		for promotion in promotions:
			product_id = promotion_id2product_id.get(promotion.id, None)
			if not product_id:
				continue

			product = id2product.get(product_id, None)
			if not product:
				continue
			product.promotions.append(promotion)