# -*- coding: utf-8 -*-

from business import model as business_model
from business.mall.promotion.intergral_sale import IntegralSale
from business.mall.promotion.flash_sale import FlashSale
from business.mall.promotion.premium_sale import PremiumSale
from db.mall import promotion_models

class PromotionRepository(business_model.Service):

	def get_promotion_by_model(self, model):
		if model.type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
			promotion = FlashSale(model)
		if model.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			promotion = PremiumSale(model)
		if model.type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
			promotion = IntegralSale(model)
		return promotion