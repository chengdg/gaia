# -*- coding: utf-8 -*-
from business import model as business_model
from business.coupon.coupon import Coupon
from db.mall import promotion_models
from eaglet.decorator import param_required
from business import model as business_model


class CouponRepository(business_model.Service):
	def get_coupon_by_id(self, coupon_id):
		db_model = promotion_models.Coupon.select().dj_where(id=coupon_id, owner_id=self.corp.id)

		coupon = Coupon.from_model({"db_model": db_model, 'corp': self.corp})

		return coupon
