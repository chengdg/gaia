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
from business.mall.category.category_product import CategoryProduct

UNLIMITED = -1

class CategoryProductRepository(object):
	"""
	获取category_product的repository
	"""
	def __init__(self, category):
		self.category = category

	@staticmethod
	def get(category):
		repository = CategoryProductRepository(category)
		return repository

	def get_top_n_products(self, n):
		"""
		获得排序靠前的n个商品
		"""
		product2relation = {}

		if n == UNLIMITED:
			product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=self.category.id).order_by('display_index')
		else:
			product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=self.category.id).order_by('display_index')[:n]

		product_ids = []
		if product_relations:
			product_ids = [relation.product_id for relation in product_relations]
			product2relation.update(dict([(relation.product_id, relation) for relation in product_relations]))

		fill_options = {
			'with_price': False,
			'with_product_model': True,
			'with_shelve_status': True
		}
		products = CorporationFactory.get().product_pool.get_products_by_ids(product_ids, fill_options)
		category_products = []
		for product in products:
			category_product = CategoryProduct(product)
			category_product.set_display_index(product2relation[product.id].display_index)
			category_products.append(category_product)

		return category_products

	def get_products(self):
		"""
		获得全部商品
		"""
		return this.get_top_n_products(UNLIMITED)