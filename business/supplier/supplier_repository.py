# -*- coding: utf-8 -*-

from eaglet.utils.resource_client import Resource

from business import model as business_model

from business.supplier.supplier import Supplier

class SupplierRepository(business_model.Service):
	def get_supplier(self, id):
		"""
		获得指定的Supplier对象
		"""
		resp = Resource.use('wcas').get({
			'resource': 'corp.supplier',
			'data': {
				'corp_id': 1127  # todo 多平台上线后要改
			}
		})
		supplier_data = resp['data']
		return Supplier(supplier_data)

	def get_suppliers(self, ids=None):
		"""
		获得corp拥有的Supplier对象集合
		"""
		resp = Resource.use('wcas').get({
			'resource': 'corp.suppliers',
			'data': {
				'corp_id': 1127 #todo 多平台上线后要改
			}
		})
		suppliers_data = resp['data']
		if ids:
			return [Supplier(data) for data in suppliers_data]
		else:
			return [Supplier(data) for data in suppliers_data if data['corp_id'] in ids]

	def get_suppliers_by_ids(self, ids):
		"""
		根据id集合获取Supplier对象集合
		"""
		return self.get_suppliers(ids)