# -*- coding: utf-8 -*-
from business import model as business_model
from business.coupon.coupon_rule import CouponRule
from db.mall import promotion_models
from eaglet.decorator import param_required
from business import model as business_model


class CouponRuleRepository(business_model.Service):
	def get_coupon_rule_by_ids(self, ids):
		db_models = promotion_models.CouponRule.select().dj_where(id__=ids, owner_id=self.corp.id)

		coupon_rules = [CouponRule.from_model({"db_model": db_model, 'corp': self.corp}) for db_model in db_models]

		return coupon_rules
