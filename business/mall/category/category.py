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
from business.mall.category.category_product_repository import CategoryProductRepository


class Category(business_model.Model):
	"""
	商品分组
	"""
	__slots__ = (
		'id',
		'name',
		'product_count',
		'display_index',
		'created_at',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		category = Category(model)
		return category

	def update_product_position(self, product_id, new_position):
		"""
		更新商品在分类中的排序位置
		"""
		mall_models.CategoryHasProduct.update(display_index=new_position).dj_where(category_id=self.id, product_id=product_id).execute()

	def delete_product(self, product_id):
		"""
		删除指定分组中的商品
		"""
		mall_models.CategoryHasProduct.delete().dj_where(category_id=self.id, product_id=product_id).execute()

		mall_models.ProductCategory.update(product_count=mall_models.ProductCategory.product_count-1).dj_where(id=self.id).execute()
		#self.context['db_model'].product_count = int(self.context['db_model'].product_count) - 1
		#self.context['db_model'].save()

	def add_products(self, product_ids):
		"""
		向分组中添加一组商品
		"""
		if product_ids:
			for product_id in product_ids:
				mall_models.CategoryHasProduct.create(
					product = product_id,
					category = self.id
				)
			mall_models.ProductCategory.update(product_count=mall_models.ProductCategory.product_count+len(product_ids)).dj_where(id=self.id).execute()

	def update_name(self, name):
		"""
		更新分组名
		"""
		mall_models.ProductCategory.update(name=name).dj_where(id=self.id).execute()		

	def get_products(self, target_page):
		"""
		获得target_page指定的CategoryProduct对象集合
		"""
		category_product_repository = CategoryProductRepository.get(self)
		category_products = category_product_repository.get_products(target_page)
		return category_products

	@property
	def top_ten_products(self):
		"""
		获得排序靠前的10个CategoryProduct对象集合
		"""
		category_product_repository = CategoryProductRepository.get(self)
		category_products = category_product_repository.get_top_n_products(10)
		return category_products

	@staticmethod
	def create(corp, name, product_ids=None):
		category_model = mall_models.ProductCategory.create(
			owner = corp.id,
			name = name,
			product_count = len(product_ids) if product_ids else 0
		)
		
		if product_ids:
			for product_id in product_ids:
				mall_models.CategoryHasProduct.create(
					product = product_id,
					category = category_model.id
				)

		return Category.from_model({
			"db_model": category_model
		})