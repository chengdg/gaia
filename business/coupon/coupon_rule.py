# -*- coding: utf-8 -*-

from datetime import datetime

from db.mall import promotion_models
from business import model as business_model

from db.mall import promotion_models
from business.mall.corporation_factory import CorporationFactory
from business.coupon.coupon_using_limit import CouponUsingLimit


class CouponRule(business_model.Model):
	"""
	优惠券
	"""

	__slots__ = (
		'id',
		'name',
		'valid_days',
		'status',
		'money',
		'coupon_count', #优惠券数量
		'receive_limit_count', #每人领取的限额
		'start_date',
		'end_date',
		'remark',
		'note',
		'product_ids',
		'remained_count',
		'receive_user_count',
		'receive_count',
		'use_count',
		'using_limit',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)

		self.context['db_model'] = model
		if model:
			self.coupon_count = model.count
			self.receive_limit_count = model.limit_counts
			self.receive_user_count = model.get_person_count
			self.receive_count = model.get_count

			self.using_limit = CouponUsingLimit(model.valid_restrictions, model.receive_rule, model.limit_product_id)
			self.status = self.__get_status(model)

	@property
	def type(self):
		if self.using_limit.is_for_specific_products:
			return 'multi_products_coupon'
		else:
			return 'all_products_coupon'

	def __get_status(self, model):
		"""
		获得优惠券规则状态
		"""
		if not model.is_active:
			return 'disabled'

		now = datetime.now()
		if now > model.end_date:
			return 'expired'

		return 'active'
		
	def update_use_count(self, count):
		"""
		增加优惠券使用数量
		"""
		promotion_models.CouponRule.update(use_count=promotion_models.CouponRule.use_count + count).dj_where(id=self.id).execute()

	def update(self, args):
		"""
		更新优惠券规则
		"""
		data = {}
		for field in ['name', 'remark', 'note']:
			if field in args:
				data[field] = args[field]

		promotion_models.CouponRule.update(**data).dj_where(id=self.id).execute()

	def disable(self):
		"""
		使优惠券规则失效
		"""
		promotion_models.CouponRule.update(is_active=False).dj_where(id=self.id).execute()		

	def add_coupons(self, count):
		"""
		向coupon rule的码库中增加count个优惠券
		"""
		coupon_rule_model = self.context['db_model']
		CorporationFactory.get().coupon_factory.create_coupons_for_rule(coupon_rule_model, count)

		self.sync_count()

	def sync_count(self):
		"""
		更新库存数量
		"""
		count = promotion_models.Coupon.select().dj_where(coupon_rule_id=self.id).count()
		remained_count = promotion_models.Coupon.select().dj_where(coupon_rule_id=self.id, status=promotion_models.COUPON_STATUS_UNGOT).count()

		promotion_models.CouponRule.update(count=count, remained_count=remained_count).dj_where(id=self.id).execute()

	def provide_to_members(self, member_ids, count_per_member):
		"""
		向会员发放优惠券
		"""
		if self.receive_limit_count > 0 and count_per_member > self.receive_limit_count:
			count_per_member = self.receive_limit_count

		if len(member_ids) * count_per_member > self.remained_count:
			return 0, u'exceed_coupon_remained_count'

		#发放优惠券
		corp = CorporationFactory.get()
		provided_count = corp.coupon_repository.provide_coupons_to_members(self.id, member_ids, count_per_member)

		#更新库存信息
		new_remained_count = self.remained_count - provided_count
		promotion_models.CouponRule.update(remained_count=new_remained_count).dj_where(id=self.id).execute()		

		return provided_count, ''

	@staticmethod
	def create(args):
		# 优惠券限制条件
		using_limit = args['using_limit']

		#使用的金额限制
		valid_restrictions = -1
		if using_limit['has_valid_restriction']:
			valid_restrictions = using_limit['valid_restrictions']


		limit_product_id = '-1'
		if using_limit['is_for_specific_products']:
			limit_product_id = ','.join([str(product_id) for product_id in using_limit['product_ids']])

		coupon_rule_model = promotion_models.CouponRule.create(
			owner = CorporationFactory.get().id,
			name = args['name'],
			money = args['money'],
			valid_restrictions = valid_restrictions,
			limit_counts= args['receive_limit_count'],
			count = args['coupon_count'],
			remained_count = args['coupon_count'],
			remark = args['remark'],
			note = args['note'],
			limit_product = using_limit['is_for_specific_products'],
			limit_product_id = limit_product_id,
			start_date = datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M'),
			end_date = datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M'),
			receive_rule= using_limit['is_no_order_user_only']
		)

		#确定新建的优惠券规则的状态
		now = datetime.now().strftime('%Y-%m-%d %H:%M')
		start_date = args['start_date']
		end_date = args['end_date']
		status = None
		if start_date <= now:
			if end_date <= now:
				status = promotion_models.PROMOTION_STATUS_FINISHED
			else:
				status = promotion_models.PROMOTION_STATUS_STARTED
		else:
			status = promotion_models.PROMOTION_STATUS_NOT_START
		#创建promotion
		promotion = promotion_models.Promotion.create(
			owner= CorporationFactory.get().id,
			promotion_title = '',
			name = args['name'],
			type = promotion_models.PROMOTION_TYPE_COUPON,
			member_grade_id = 0,
			status = status,
			start_date = args['start_date'],
			end_date = args['end_date'],
			detail_id= coupon_rule_model.id
		)
		
		coupon_rule = CouponRule(coupon_rule_model)
		coupon_rule.add_coupons(int(args['coupon_count']))

		return coupon_rule
