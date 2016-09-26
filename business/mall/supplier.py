# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.account import models as account_models
from business import model as business_model


class Supplier(business_model.Model):
	"""
	封装mall_supplier和auth_user两种供货商
	"""

	__slots__ = (
		'id',
		'name',
		'owner_id',
		'responsible_person',
		'supplier_tel',
		'supplier_address',
		'remark',
		'is_delete',
		'created_at',
		'type'  # supplier,user(对应auth_user，仅有历史数据
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	# @staticmethod
	# @param_required(['db_model'])
	# def from_model(args):
	#     model = args['db_model']
	#     product = Supplier(model)
	#     return product
	#
	# @staticmethod
	# @param_required(['id'])
	# def from_id(args):
	#     supplier_db_model = mall_models.Supplier.get(id=args['id'])
	#     return Supplier(supplier_db_model)
	#
	# @staticmethod
	# @param_required(['ids'])
	# def from_ids(args):
	#     supplier_db_models = mall_models.Supplier.select.dj_where(id__in=args['ids'])
	#     suppliers = []
	#     for model in supplier_db_models:
	#         suppliers.append(Supplier(model))
	#     return suppliers
	#
	# @staticmethod
	# @param_required(['ids'])
	# def get_id_2_supplier_name(args):
	#     supplier_db_models = mall_models.Supplier.select().dj_where(id__in=args['ids'])
	#     id2supplier_name = {}
	#     for model in supplier_db_models:
	#         id2supplier_name[model.id] = model.name
	#     return id2supplier_name
	#
	# def save(self):
	#     """
	#     """
	#     # 'name', 'responsible_person', 'supplier_tel', 'supplier_address', 'remark'
	#     new_model = mall_models.Supplier.create(owner=self.owner_id,
	#                                             name=self.name,
	#                                             responsible_person=self.responsible_person,
	#                                             supplier_tel=self.supplier_tel,
	#                                             supplier_address=self.supplier_address,
	#                                             remark=self.remark)
	#     return Supplier(new_model)
	#
	# def update(self):
	#     change_rows = mall_models.Supplier.update(name=self.name,
	#                                               remark=self.remark,
	#                                               responsible_person=self.responsible_person,
	#                                               supplier_tel=self.supplier_tel,
	#                                               supplier_address=self.supplier_address,
	#                                               ).dj_where(id=self.id).execute()
	#     return change_rows

	@staticmethod
	@param_required(['id', 'type'])
	def from_id(args):
		type = args['type']
		if type == 'user':
			return Supplier.__from_user(args['id'])
		elif type == 'supplier':
			return Supplier.__from_supplier(args['id'])
		supplier_db_model = mall_models.Supplier.get(id=args['id'])
		return Supplier(supplier_db_model)

	@staticmethod
	def __from_user(id):
		supplier = Supplier()
		db_model = account_models.UserProfile.get(id=id)
		supplier.type = 'user'
		supplier.name = db_model.store_name
		supplier.id = db_model.user_id
		return supplier

	@staticmethod
	def __from_supplier(id):
		supplier_db_model = mall_models.Supplier.get(id=id)
		supplier = Supplier(supplier_db_model)
		supplier.type = 'supplier'


		return supplier
