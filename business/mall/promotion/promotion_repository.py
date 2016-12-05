# -*- coding: utf-8 -*-
from db.mall import promotion_models
from business import model as business_model
from business.mall.promotion.promotion import Promotion
from business.mall.promotion.fill_promotion_detail_service import FillPromotionDetailService

class PromotionRepository(business_model.Service):

	def get_promotion_by_ids(self, promotion_ids, fill_options=None):
		models = promotion_models.Promotion.select().dj_where(id__in=promotion_ids)
		promotions = [Promotion(model) for model in models]
		fill_promotion_detail_service = FillPromotionDetailService(self.corp)
		fill_promotion_detail_service.fill_detail(promotions, self.corp, fill_options)
		return promotions

	def delete_promotions(self, promotion_ids):
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_DELETED
		).dj_where(id__in=promotion_ids).execute()
		return True

	def get_promotion_by_id(self, promotion_id, fill_options=None):
		promotions = self.get_promotion_by_ids([promotion_id], fill_options=fill_options)
		return promotions[0] if promotions else None
