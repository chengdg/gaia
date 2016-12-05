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

	def search_premium_sale_promotions(self, page_info, fill_options=None, filters=None):
		"""
		搜索买赠的促销活动
		"""
		filters = filters if filters else {}
		filters['type'] = promotion_models.PROMOTION_TYPE_PREMIUM_SALE
		promotions, pageinfo = self.get_promotions(page_info, fill_options=fill_options, filters=fill_options)
		return promotions, page_info

	def get_promotions(self, page_info, fill_options=None, options=None, filters=None):
		pass

	def active_promotion(self, promotion_ids):
		"""
        开启促销活动
        promotion_ids: [promtion_id,...]
        """
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_DELETED
		).dj_where(id__in=promotion_ids).execute()
		return True

	def off_promotion(self, promotion_ids):
		"""
        关闭撤销活动
        """
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_FINISHED
		).dj_where(id__in=promotion_ids).execute()
		return True
