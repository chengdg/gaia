# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.product import Product

class CategoryHasProduct(business_model.Model):
	'''
	分组领域中商品值对象
	'''
	__slots__ =  (
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
	def emptyCateogryHasProduct(model=None):
		category_has_product_obj = CategoryHasProduct(model)
		return category_has_product_obj

	@staticmethod
	@param_required(['category_has_product_id'])
	def fromId(args):
		category_has_product_obj = mall_models.CategoryHasProduct.select().dj_where(id=args['category_has_product_id'])
		if category_has_product_obj.first():
			return CategoryHasProduct(category_has_product_obj.first())
		else:
			return None

	def save(self, category_obj, product_obj):
			opt = {
				'product': product_obj.context['db_model'],
				'category': category_obj.context['db_model']
			}
		   # created is True or False  
			# If an object is found, get_or_create() returns a tuple of that object and False. 
			# If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
			# If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
			obj, created = mall_models.CategoryHasProduct.get_or_create(**opt)
			return CategoryHasProduct(obj)

	def deleteFromId(self, category_has_product_id):
		category_has_product_obj = mall_models.CategoryHasProduct.get(id=category_has_product_id)
		return category_has_product_obj.delete_instance()

	def deleteFromModel(self, category_obj):
		mall_models.CategoryHasProduct.get(category=category_obj.context['db_model']).delete_instance()

	@staticmethod
	@param_required(['category_id', 'product_id'])
	def  fromCategoryIdAndProduct_id(args):
		category_has_product_obj = mall_models.CategoryHasProduct.select().dj_where(category_id=args['category_id'], product_id=args['product_id'])
		if category_has_product_obj.first():
			return CategoryHasProduct(category_has_product_obj.first())
		else:
			return None

	def updatePosition(self, category_id ,product_id, position):
	   mall_models.CategoryHasProduct.update(display_index=position).dj_where(product_id=product_id, category_id=category_id).execute()

	@property
	def category(self):
		category_has_product_obj = self.context['db_model']
		return category_has_product_obj.category

	@property
	def product(self):
		category_has_product_obj = self.context['db_model']
		return category_has_product_obj.product


