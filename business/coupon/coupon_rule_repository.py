# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import paginator

from business import model as business_model
from business.coupon.coupon_rule import CouponRule
from business import model as business_model
from db.mall import promotion_models

class CouponRuleRepository(business_model.Service):
	def get_coupon_rules(self, filter, page_info):
		"""
		获得corp所有的coupon rule集合
		"""
		promotions = promotion_models.Promotion.select().dj_where(owner_id=self.corp.id, type=promotion_models.PROMOTION_TYPE_COUPON, status__not=promotion_models.PROMOTION_STATUS_DELETED).order_by(-promotion_models.Promotion.id)
		pageinfo, promotions = paginator.paginate(promotions, page_info.cur_page, page_info.count_per_page)

		coupon_rule_ids = [promotion.detail_id for promotion in promotions]
		db_models = list(promotion_models.CouponRule.select().dj_where(owner_id=self.corp.id, id__in=coupon_rule_ids))
		db_models.sort(lambda x,y: cmp(y.id, x.id))

		coupon_rules = [CouponRule(db_model) for db_model in db_models]

		return coupon_rules, pageinfo

	def get_coupon_rule_by_ids(self, ids):
		"""
		获得corp中由ids指定的coupon rule集合
		"""
		db_models = promotion_models.CouponRule.select().dj_where(id__in=ids, owner_id=self.corp.id)

		coupon_rules = [CouponRule(db_model) for db_model in db_models]

		return coupon_rules

	def get_coupon_rule_by_id(self, id):
		"""
		获得corp中由id指定的coupon rule对象
		"""
		return self.get_coupon_rule_by_ids([id])[0]

	def delete_coupon_rule(self, id):
		"""
		删除coupon rule
		"""
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_DELETED
		).dj_where(detail_id=id).execute()
