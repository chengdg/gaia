# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.corporation_factory import CorporationFactory
from business.mall.supplier.divide_rebate_info import DivideRebateInfo
from business.mall.supplier.retail_rebate_info import RetailRebateInfo

TYPEINT2TYPESTR = {
	mall_models.SUPPLIER_TYPE_DIVIDE: 'divide',
	# 零售返点
	mall_models.SUPPLIER_TYPE_RETAIL: 'retail',
	# 固定低价
	mall_models.SUPPLIER_TYPE_FIXED: 'fixed',
	# 普通供货商
	mall_models.SUPPLIER_TYPE_NORMAL: 'normal'
}

SETTLEMENTINT2SETTLEMENTSTR = {
	mall_models.SUPPLIER_SETTLEMENT_PERIOD_MONTH: 'month',
	mall_models.SUPPLIER_SETTLEMENT_PERIOD_15TH_DAY: '15day',
	mall_models.SUPPLIER_SETTLEMENT_PERIOD_WEEK: 'week'
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
		'type'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.type = TYPEINT2TYPESTR.get(model.type, 'unknown')
			self.settlement_period = SETTLEMENTINT2SETTLEMENTSTR.get(model.settlement_period, 'unknown')

	def is_divide_type(self):
		"""
		是否是分成模式的供应商
		"""
		return self.type == 'divide'

	def get_divide_info(self):
		"""
		获得分成模式信息
		"""
		if '__divide_info' in self.context:
			return self.context['__divide_info']
		else:
			divide_info = DivideRebateInfo(mall_models.SupplierDivideRebateInfo.select().dj_where(supplier_id=self.id).get())
			self.context['__divide_info'] = divide_info
			return divide_info

	def set_divide_info(self, divide_info):
		self.context['__divide_info'] = divide_info

	def is_retail_type(self):
		"""
		是否是零售返点模式的供货商
		"""
		return self.type == 'retail'

	def get_retail_info(self):
		"""
		获得零售返点模式的供货商
		"""
		if '__retail_info' in self.context:
			return self.context['__retail_info']
		else:
			retail_info = RetailRebateInfo(mall_models.SupplierRetailRebateInfo.select().dj_where(supplier_id=self.id).get())
			self.context['__retail_info'] = retail_info
			return retail_info

	def set_retail_info(self, retail_info):
		self.context['__retail_info'] = retail_info

	@staticmethod
	@param_required(['name', 'responsible_person', 'supplier_tel', 'supplier_address', 'remark', 'type', 'settlement_period'])
	def create(args):
		"""
		保存信息
		"""
		corp_id = CorporationFactory.get().id

		supplier_type = args['type']
		if supplier_type == 'divide':
			supplier_type = mall_models.SUPPLIER_TYPE_DIVIDE
		elif supplier_type == 'retail':
			supplier_type = mall_models.SUPPLIER_TYPE_RETAIL
		elif supplier_type == 'fixed':
			supplier_type = mall_models.SUPPLIER_TYPE_FIXED
		else:
			supplier_type = mall_models.SUPPLIER_TYPE_NORMAL

		settlement_period = args['settlement_period']
		if settlement_period == '15day':
			settlement_period = mall_models.SUPPLIER_SETTLEMENT_PERIOD_15TH_DAY
		elif settlement_period == 'week':
			settlement_period = mall_models.SUPPLIER_SETTLEMENT_PERIOD_WEEK
		else:
			settlement_period = mall_models.SUPPLIER_SETTLEMENT_PERIOD_MONTH

		model = mall_models.Supplier.create(
			owner = corp_id,
			name = args['name'],
			responsible_person = args['responsible_person'],
			supplier_tel = args['supplier_tel'],
			supplier_address = args['supplier_address'],
			remark = args['remark'],
			type = supplier_type,
			settlement_period = settlement_period
		)
		supplier = Supplier(model)

		if args['type'] == 'divide':
			#创建divide info
			divide_info = args['divide_info']
			divide_rebate_info_model = mall_models.SupplierDivideRebateInfo.create(
				supplier_id = model.id,
				divide_money = divide_info['divide_money'],
				basic_rebate = divide_info['basic_rebate'],
				rebate = divide_info['rebate']
			)
			supplier.set_divide_info(DivideRebateInfo(divide_rebate_info_model))
		elif args['type'] == 'retail':
			#创建retail info
			retail_info = args['retail_info']
			retail_rebate_info_model = mall_models.SupplierRetailRebateInfo.create(
				supplier_id = model.id,
				rebate = retail_info['rebate']
			)
			supplier.set_retail_info(RetailRebateInfo(retail_rebate_info_model))

		return supplier

