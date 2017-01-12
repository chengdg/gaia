# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator

from business.mall.corporation_factory import CorporationFactory

class Shipper(business_model.Model):
	"""
	发货人
	"""
	__slots__ = (
		'id',
		'name',
		'tel_number',
		'province',
		'city',
		'district',
		'address',
		'postcode',
		'company_name',
		'remark' ,
		'is_active',	
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['name','tel_number','province','city','district','address','postcode','company_name','remark','is_active'])
	def create(args):

		corp_id = CorporationFactory.get().id

		shipper = mall_models.ShipperMessages.create(
			owner=corp_id,
			name = args['name'],
			tel_number = args['tel_number'],
			province = args['province'],
			city = args['city'],
			district = args['district'],
			address = args['address'],
			postcode = args['postcode'],
			company_name = args['company_name'],
			remark = args['remark'],
			is_active = args['is_active'],
		)
		return Shipper(shipper)

	def update(self,name,tel_number,province,city,district,address,postcode,company_name,remark,is_active):
	
		corp_id = CorporationFactory.get().id

		shipper = mall_models.ShipperMessages.update(
			name = name,
			tel_number = tel_number,
			province = province,
			city = city,
			district = district,
			address = address,
			postcode = postcode,
			company_name = company_name,
			remark = remark,
			is_active = is_active,
		).dj_where(id=self.id).execute()
		return Shipper(shipper)

	def set_used(self):
			"""
			将当前发货人设置为"使用"
			"""
			mall_models.ShipperMessages.update(is_active=False).dj_where(id__not=self.id).execute()
			mall_models.ShipperMessages.update(is_active=True).dj_where(id=self.id).execute()