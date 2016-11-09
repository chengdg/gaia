# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator

from business.product.product import Product
from business.mall.corporation_factory import CorporationFactory


class CategoryProduct(business_model.Model):
	"""
	分类中的商品
	"""
	__slots__ = (
		'id',
		'name',
		'price',
		'display_index',
		'status',
		'sales',
		'categories',
		'created_at'
	)

	def __init__(self, product=None):
		business_model.Model.__init__(self)

		self.context['product'] = product
		if product:
			self._init_slot_from_model(product)
			if product.is_on_shelve():
				self.status = 'on_shelf'
			elif product.shelve_type == 'in_pool':
				self.status = 'in_pool'
			elif product.shelve_type == 'deleted':
				self.status = 'deleted'
			else:
				self.status = 'off_shelf'

			#获取价格
			self.price = product.price_info['display_price']

	@staticmethod
	def from_product(product):
		return CategoryProduct(product)

	def set_display_index(self, index):
		self.display_index = index