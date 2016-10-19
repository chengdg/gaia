# -*- coding: utf-8 -*-
from business import model as business_model
from business.coupon.coupon_rule import CouponRule
from db.mall import promotion_models
from eaglet.decorator import param_required
from business import model as business_model


class CouponRuleRepository(business_model.Service):
	def get_coupon_by_id(self, id):
		db_model = promotion_models.CouponRule.select().dj_where(id=id, owner_id=self.corp.id)

		coupon_rule = CouponRule.from_model({"db_model": db_model, 'corp': self.corp})

		return coupon_rule
