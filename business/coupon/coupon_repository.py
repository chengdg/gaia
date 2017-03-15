# -*- coding: utf-8 -*-
from datetime import datetime

from eaglet.core import paginator

from db.mall import promotion_models
from business import model as business_model
from business.coupon.coupon import Coupon
from business import model as business_model
from business.mall.corporation_factory import CorporationFactory


class CouponRepository(business_model.Service):
	def get_coupons_for_rule(self, coupon_rule_id, filters, page_info):
		"""
		获得rule中的coupon的集合
		"""
		coupon_models = promotion_models.Coupon.select().dj_where(coupon_rule_id=coupon_rule_id)
		pageinfo, coupon_models = paginator.paginate(coupon_models, page_info.cur_page, page_info.count_per_page)

		coupons = [Coupon(coupon_model) for coupon_model in coupon_models]

		return coupons, pageinfo

	def get_coupon_by_id(self, coupon_id):
		"""
		根据coupon_id获得优惠券
		"""
		coupons = self.get_coupons_by_ids([coupon_id])
		if len(coupons) > 0:
			return coupons[0]
		else:
			return None

	def get_coupons_by_ids(self, coupon_ids):
		"""
		根据coupon_ids获得优惠券集合
		"""
		db_models = promotion_models.Coupon.select().dj_where(id__in=coupon_ids, owner_id=self.corp.id)
		return [Coupon(db_model) for db_model in db_models]

	def get_coupons_for_member(self, member, page_info):
		"""
		获得属于会员的优惠券集合
		"""
		corp = CorporationFactory.get()
		orders = corp.order_repository.get_orders_for_member(member)
		order_coupon_ids = [order.coupon_id for order in orders if order.coupon_id > 1]

		if len(order_coupon_ids) > 0:
			coupon_models = list(promotion_models.Coupon.select().where(
				(promotion_models.Coupon.member_id == member.id) | (promotion_models.Coupon.id.in_(order_coupon_ids))
			).order_by(-promotion_models.Coupon.provided_time))
		else:
			coupon_models = list(promotion_models.Coupon.select().dj_where(member_id=member.id).order_by(-promotion_models.Coupon.provided_time))

		pageinfo, coupon_models = paginator.paginate(coupon_models, page_info.cur_page, page_info.count_per_page)

		coupons = [Coupon(coupon_model) for coupon_model in coupon_models]
		coupons.sort(lambda x,y: cmp(y.received_time, x.received_time))

		return coupons, pageinfo

	def delete_coupons(self, coupon_ids):
		"""
		删除由coupon_ids指定的coupon
		"""
		if len(coupon_ids) > 0:
			#获得coupon rule，删除优惠券后更新其库存数量
			coupon_rule = self.get_coupon_by_id(coupon_ids[0]).rule

			promotion_models.Coupon.delete().dj_where(id__in=coupon_ids, owner_id=self.corp.id).execute()
			
			coupon_rule.sync_count()

		return True

	def provide_coupons_to_members(self, coupon_rule_id, member_ids, count_per_member):
		"""
		向指定的会员发放优惠券
		"""
		count = len(member_ids) * count_per_member
		coupons = promotion_models.Coupon.select().dj_where(coupon_rule_id=coupon_rule_id)[:count]
		now = datetime.now()
		for i, member_id in enumerate(member_ids):
			for j in range(count_per_member):
				index = i*count_per_member + j
				coupon = coupons[index]
				promotion_models.Coupon.update(
					member_id = member_id, 
					status = promotion_models.COUPON_STATUS_UNUSED,
					provided_time = now
				).dj_where(id=coupon.id).execute()
		
		return len(coupons)
