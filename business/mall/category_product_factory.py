# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.category_product import CategoryProduct
from business.mall.product import Product


class CategoryProductFactory(business_model.Model):
	'''
	创建分组中商品关系@生成器
	'''
	__slots__ = ()

	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	def create():
		category_product = CategoryProductFactory()
		return category_product

	def save(self, product_ids, category_obj):
		category_products = []
		category_product = CategoryProduct.emptyCateogryHasProduct()
		for product_id in product_ids:
			product = Product.from_id({'product_id': product_id})
			category_product = category_product.save(
				category_obj, product)
			category_products.append(category_has_product)
		return category_products
