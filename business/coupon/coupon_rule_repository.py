# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import paginator

from business import model as business_model
from business.coupon.coupon_rule import CouponRule
from business import model as business_model
from db.mall import promotion_models
from business.common.filter_parser import FilterParser

class CouponRuleRepository(business_model.Service):
	def __split_filters(self, filters):
		promotion_filter_values = {}
		coupon_rule_filter_values = {}
		coupon_filter_values = {}
		filter_parse_result = FilterParser.get().parse(filters)

		should_use_default_status = True

		for filter_field_op, filter_value in filter_parse_result.items():
			items = filter_field_op.split('__')
			filter_field = items[0]
			op = None
			if len(items) > 1:
				op = items[1]
			filter_category = None
			should_ignore_field = False
			if filter_field == 'status':
				filter_category = promotion_filter_values
				should_use_default_status = False
				if filter_value == 'not_start':
					filter_value = promotion_models.PROMOTION_STATUS_NOT_START
				elif filter_value == 'running':
					filter_value = promotion_models.PROMOTION_STATUS_STARTED
				elif filter_value == 'finished':
					filter_value = promotion_models.PROMOTION_STATUS_FINISHED
				elif filter_value == 'disalbed':
					filter_value = promotion_models.PROMOTION_STATUS_DISABLE
			elif filter_field == 'name':
				filter_category = promotion_filter_values
			elif filter_field == 'type':
				filter_category = coupon_rule_filter_values
				if filter_value == 'general':
					filter_value = False
				else:
					filter_value = True
				filter_field_op = 'limit_product'
			elif filter_field == 'promotion_date':
				filter_category = promotion_filter_values
				start_date, end_date = filter_value
				if start_date:
					filter_category['start_date__gte'] = start_date
				if end_date:
					filter_category['end_date__lte'] = end_date
				should_ignore_field = True
			elif filter_field == 'coupon_bid':
				filter_category = coupon_filter_values
				filter_field_op = 'coupon_id'

			if not should_ignore_field:
				if op:
					filter_field_op = '%s__%s' % (filter_field, op)
				filter_category[filter_field_op] = filter_value
		
		#填充默认的搜索参数
		promotion_filter_values['owner_id'] = self.corp.id
		promotion_filter_values['type'] = promotion_models.PROMOTION_TYPE_COUPON
		if should_use_default_status:
			promotion_filter_values['status__not'] = promotion_models.PROMOTION_STATUS_DELETED

		return {
			'coupon_rule': coupon_rule_filter_values,
			'coupon': coupon_filter_values,
			'promotion': promotion_filter_values,
		}

	def get_coupon_rules(self, filters, page_info):
		"""
		获得corp所有的coupon rule集合
		"""
		type2fiters = self.__split_filters(filters=filters)

		if type2fiters['coupon']:
			coupons = promotion_models.Coupon.select().dj_where(**type2fiters['coupon'])
			coupon_rule_ids = [coupon.coupon_rule_id for coupon in coupons]
			db_models = promotion_models.CouponRule.select().dj_where(id__in=coupon_rule_ids)
			pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)
			db_models = list(db_models)
		else:
			#获得按promotion过滤后的coupon rule
			promotion_filters = type2fiters['promotion']
			coupon_rule_ids = None
			if promotion_filters:
				promotions = promotion_models.Promotion.select().dj_where(**promotion_filters)

			coupon_rule_filters = type2fiters['coupon_rule']
			if len(coupon_rule_filters) == 0:
				#不用搜索其他属性，直接分页
				pageinfo, promotions = paginator.paginate(promotions, page_info.cur_page, page_info.count_per_page)
				coupon_rule_ids = [promotion.detail_id for promotion in promotions]
				db_models = list(promotion_models.CouponRule.select().dj_where(owner_id=self.corp.id, id__in=coupon_rule_ids))
			else:
				#还需搜索coupon rule其他属性
				coupon_rule_ids = [promotion.detail_id for promotion in promotions]
				coupon_rule_filters['id__in'] = coupon_rule_ids
				coupon_rule_filters['owner_id'] = self.corp.id
				db_models = promotion_models.CouponRule.select().dj_where(**coupon_rule_filters)
				pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)
				db_models = list(db_models)

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
