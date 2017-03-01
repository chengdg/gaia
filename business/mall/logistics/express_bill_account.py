# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator

from business.mall.corporation_factory import CorporationFactory

class ExpressBillAccount(business_model.Model):
	"""
	电子面单
	"""
	__slots__ = (
		'id',
		'express_name',
		'customer_name',
		'customer_pwd',
		'logistics_number',
		'sendsite',
		'remark',	
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['express_name','customer_name','customer_pwd','logistics_number','sendsite','remark'])
	def create(args):

		corp_id = CorporationFactory.get().id

		express_bill_account = mall_models.ExpressBillAccount.create(
			owner=corp_id,
			express_name = args['express_name'],
			customer_name = args['customer_name'],
			customer_pwd = args['customer_pwd'],
			logistics_number = args['logistics_number'],
			sendsite = args['sendsite'],
			remark = args['remark']
		)
		return ExpressBillAccount(express_bill_account)

	def update(self,express_name,customer_name,customer_pwd,logistics_number,sendsite,remark):

		express_bill_account = mall_models.ExpressBillAccount.update(
			express_name = express_name,
			customer_name = customer_name,
			customer_pwd = customer_pwd,
			logistics_number = logistics_number,
			sendsite = sendsite,
			remark = remark
		).dj_where(id=self.id).execute()
		return ExpressBillAccount(express_bill_account)
