# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.category import Category
from business.mall.product import Product

class CategoryFactory(business_model.Model):
	'''
	分组创建工厂@生成器
	'''
	__slots__=()
	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	def create():
		category_factory = CategoryFactory()
		return category_factory

	def save(self, owner_id, name, product_ids=None):
		category = Category.empty_category()
		if product_ids:
			product_ids = [product_id.strip() for product_id in product_ids.strip().split(',') if product_id]
			products = Product.from_ids({'product_ids': product_ids})
		else:
			products = product_ids
		return category.save(owner_id, name, products)


