# -*- coding: utf-8 -*-
"""
积分应用
"""
from business import model as business_model
from business.mall.promotion.integral_sale_rule import IntegralSaleRule


class IntegralSale(business_model.Model):
	"""
	积分应用
	"""
	__slots__ = (
		'integral_sale_type',
		'display_integral_sale_type',
		'is_permanant_active',
		'rules',
		'discount',
		'discount_money'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		self._init_slot_from_model(db_model)

	def add_rule(self, integral_sale_rule_model):
		"""
		向integral sale促销中添加`积分应用规则`
		"""
		if self.rules is None:
			self.rules = []

		rule = IntegralSaleRule(integral_sale_rule_model)
		self.rules.append(rule.to_dict())

	def calculate_discount(self):
		"""
		计算折扣信息
		"""
		if len(self.rules) == 0:
			discount = 0
			discount_money = 0
		elif len(self.rules) == 1:
			rule = self.rules[0]
			discount = str(rule['discount']) + '%'
			discount_money = "%.2f" % rule['discount_money']
		else:
			discounts = [rule['discount'] for rule in self.rules]
			max_discount = max(discounts)
			min_discount = min(discounts)

			discount_moneys = [rule['discount_money'] for rule in self.rules]
			max_discount_money = max(discount_moneys)
			min_discount_money = min(discount_moneys)

			if max_discount == min_discount:
				discount = str(max_discount)
			else:
				discount = '%d%% ~ %d%%' % (min_discount, max_discount)

			if max_discount_money == min_discount_money:
				discount_money = str(max_discount_money)
			else:
				discount_money = '%.2f ~ %.2f' % (min_discount_money, max_discount_money)

		self.discount = discount
		self.discount_money = discount_money