# -*- coding: utf-8 -*-
from db.mall import promotion_models
from business import model as business_model
from business.mall.promotion.promotion import Promotion


class PromotionRepository(business_model.Service):

	def get_promotion(self, model):
		promotion = Promotion(model)
		return promotion