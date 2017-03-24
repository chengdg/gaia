# -*- coding: utf-8 -*-

from business import model as business_model

from business.supplier.retail_rebate_info import RetailRebateInfo

TYPEINT2TYPESTR = {
	'divide': 3,
	# 零售返点
	'retail': 2,
	# 固定低价
	'fixed': 1,
	# 高佣直采
	'mining': 4,
	# 普通供货商
	'normal': 0
}

SETTLEMENTINT2SETTLEMENTSTR = {
	'month': 1,
	'15day': 2,
	'week': 3
}

class Supplier(business_model.Model):
	"""
	供货商
	"""
	__slots__ = (
		'id',
		'name',
		'responsible_person',
		'supplier_tel',
		'supplier_address',
		'remark',
		'is_delete',
		'created_at',
		'settlement_period',
		'type',
		'divide_rebate'
	)

	def __init__(self, data):
		business_model.Model.__init__(self)

		if data:
			self.id = int(data['corp_id'])
			self.name = data['name']
			self.responsible_person = data['axe_sales_name']
			self.type = int(data['settlement_type'])
			self.settlement_period = data['clear_period']
			self.created_at = data['created_at']
			self.is_delete = data['status']
			self.divide_rebate = data['divide_rebate']


	def is_retail_type(self):
		"""
		是否是零售返点模式的供货商
		"""
		return self.type == TYPEINT2TYPESTR['retail']

	def get_retail_info(self):
		"""
		获得零售返点模式的供货商
		"""
		if '__retail_info' in self.context:
			return self.context['__retail_info']
		else:
			retail_info = RetailRebateInfo(self.divide_rebate)
			self.context['__retail_info'] = retail_info
			return retail_info

	def set_retail_info(self, retail_info):
		self.context['__retail_info'] = retail_info


