# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model

class ExpressDeliveryCompany(business_model.Model):
	"""
	快递公司名称
	"""
	__slots__ = (
		'company_id',
		'name',
		'value',
		'kdniao_value'
	)

	def __init__(self, company_id, name, value, kdniao_value):
		self.company_id = company_id
		self.name = name
		self.value = value
		self.kdniao_value = kdniao_value