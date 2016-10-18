# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model

from business.mall.corporation_factory import CorporationFactory
from business.mall.supplier.supplier import Supplier
from business.mall.supplier.divide_rebate_info import DivideRebateInfo
from business.mall.supplier.retail_rebate_info import RetailRebateInfo

class SupplierRepository(business_model.Service):
	def get_supplier(self, id):
		"""
		获得指定的Supplier对象
		"""
		model = mall_models.Supplier.select().dj_where(owner_id=self.corp.id, id=id).get()
		return Supplier(model)

	def get_suppliers(self):
		"""
		获得corp拥有的Supplier对象集合
		"""
		models = mall_models.Supplier.select().dj_where(owner_id=self.corp.id)
		return [Supplier(model) for model in models if not model.is_delete]

	def get_suppliers_by_ids(self, ids):
		"""
		根据id集合获取Supplier对象集合
		"""
		suppliers = [Supplier(model) for model in mall_models.Supplier.select().dj_where(id__in=ids)]

		id2supplier = dict()
		divide_type_supplier_ids = []
		retail_type_supplier_ids = []
		for supplier in suppliers:
			id2supplier[supplier.id] = supplier

			if supplier.type == mall_models.SUPPLIER_TYPE_DIVIDE:
				divide_type_supplier_ids.append(supplier.id)
			elif supplier.type == mall_models.SUPPLIER_TYPE_RETAIL:
				retail_type_supplier_ids.append(supplier.id)
			else:
				pass

		divide_info_models = mall_models.SupplierDivideRebateInfo.select().dj_where(supplier_id__in=divide_type_supplier_ids)
		for model in divide_info_models:
			id2supplier[model.supplier_id].set_divide_info(DivideRebateInfo(model))

		retail_info_models = mall_models.SupplierRetailRebateInfo.select().dj_where(supplier_id__in=retail_type_supplier_ids)
		for model in retail_info_models:
			id2supplier[model.supplier_id].set_retail_info(RetailRebateInfo(model))

		return suppliers

	def delete_supplier(self, id):
		"""
		删除指定的供货商
		"""
		mall_models.Supplier.update(is_delete=True).dj_where(owner_id=self.corp.id, id=id).execute()
