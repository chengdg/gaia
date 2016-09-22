# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models
from business.product.product_shelf import ProductShelf
from business.product.product_pool import ProductPool


class Corporation(business_model.Model):
	"""
	商家
	"""
	__slots__ = (
		'id',
		'name'
	)

	def __init__(self, owner_id):
		self.id = owner_id
		self.name = 'unknown'

	@property
	def insale_shelf(self):
		product_shelf = ProductShelf.get({
			"corp": self,
			'type': 'in_sale'
		})

		return product_shelf

	@property
	def forsale_shelf(self):
		product_shelf = ProductShelf.get({
			"corp": self,
			'type': 'for_sale'
		})

		return product_shelf

	@property
	def product_pool(self):
		return ProductPool.get_for_corp({
			"corp": self
		})