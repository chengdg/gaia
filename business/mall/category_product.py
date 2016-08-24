# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.product import Product


class CategoryProduct(business_model.Model):
	'''
	分组领域中商品值对象
	'''
	__slots__ = (
		'id',
		'product_id',
		'category_id',
		'display_index',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	def empty_cateogry_product(model=None):
		category_product = CategoryProduct(model)
		return category_product

	@staticmethod
	@param_required(['category_product_id'])
	def from_id(args):
		category_product = mall_models.CategoryHasProduct.select().dj_where(id=args[
			'category_product_id'])
		if category_product.first():
			return CategoryProduct(category_product.first())
		else:
			return None

	def save(self, category, product):
		opt = {
			'product': product.context['db_model'],
			'category': category.context['db_model']
		}
		# created is True or False
		# If an object is found, get_or_create() returns a tuple of that object and False.
		# If multiple objects are found, get_or_create raises MultipleObjectsReturned.
		# If an object is not found, get_or_create() will instantiate and save
		# a new object, returning a tuple of the new object and True
		obj, created = mall_models.CategoryHasProduct.get_or_create(**opt)
		return CategoryProduct(obj)

	def delete_from_id(self, category_product_id):
		category_product = mall_models.CategoryHasProduct.get(
			id=category_product_id)
		return category_product.delete_instance()

	def delete_from_model(self, category):
		mall_models.CategoryHasProduct.get(category=category.context['db_model']).delete_instance()

	@staticmethod
	@param_required(['category_id', 'product_id'])
	def from_category_id_and_product_id(args):
		category_product = mall_models.CategoryHasProduct.select().dj_where(
			category_id=args['category_id'], product_id=args['product_id'])
		if category_product.first():
			return CategoryProduct(category_product.first())
		else:
			return None

	def update_position(self, category_id, product_id, position):
		mall_models.CategoryHasProduct.update(display_index=position).dj_where(
			product_id=product_id, category_id=category_id).execute()

	@property
	def category(self):
		category_product = self.context['db_model']
		return category_product.category

	@property
	def product(self):
		category_product = self.context['db_model']
		return category_product.product
