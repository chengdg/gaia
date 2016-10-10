# coding=utf-8
# -*- utf-8 -*-
from eaglet.decorator import param_required

from bdem import msgutil
from business import model as business_model

from business.product.product import Product
from db.mall import models as mall_models

class ProductProperty(business_model.Model):
	"""
	商品属性
	"""
	__slots__ = (
		'name',
		'value'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)
