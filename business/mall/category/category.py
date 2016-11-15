# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy
from bdem import msgutil

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator

from business.product.product import Product
from business.mall.corporation_factory import CorporationFactory
from business.mall.category.category_product_repository import CategoryProductRepository
from gaia_conf import TOPIC

MAX_DISPLAY_INDEX = 9999999


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
		#将已经占用new_position的商品置为MAX_DISPLAY_INDEX
		mall_models.CategoryHasProduct.update(display_index=MAX_DISPLAY_INDEX).dj_where(category_id=self.id, display_index=new_position).execute()

		#将目标商品的position置为new_position
		mall_models.CategoryHasProduct.update(display_index=new_position).dj_where(category_id=self.id, product_id=product_id).execute()

	def __update_product_count(self):
		"""
		更新category中的product count
		"""
		new_count = mall_models.CategoryHasProduct.select().dj_where(id=self.id).count()
		mall_models.ProductCategory.update(product_count=new_count).dj_where(id=self.id).execute()

	def delete_product(self, product_id):
		"""
		删除指定分组中的商品
		"""
		mall_models.CategoryHasProduct.delete().dj_where(category_id=self.id, product_id=product_id).execute()

		self.__update_product_count()

		msgutil.send_message(
			TOPIC['product'],
			'delete_product_from_category',
			{
				'corp_id': CorporationFactory.get().id,
				'product_id': product_id,
				'category_id': self.id
			}
		)

	def add_products(self, product_ids):
		"""
		向分组中添加一组商品

		先过滤出CategoryHasProduct表中已经存在的<category_id, product_id>对，只向表中添加新的<category_id, product_id>对
		"""
		if product_ids:
			relations = mall_models.CategoryHasProduct.select().dj_where(product_id__in=product_ids, category_id=self.id)
			existed_product_ids = set([relation.product_id for relation in relations])

			product_ids = set(product_ids)
			new_product_ids = product_ids - existed_product_ids

			if new_product_ids:
				for product_id in new_product_ids:
					mall_models.CategoryHasProduct.create(
						product = product_id,
						category = self.id
					)
				
				self.__update_product_count()
				
				msgutil.send_message(
					TOPIC['product'],
					'add_products_to_category',
					{
						'corp_id': CorporationFactory.get().id,
						'product_ids': new_product_ids,
						'category_id': self.id
					}
				)
		
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

			msgutil.send_message(
				TOPIC['product'],
				'add_products_to_category',
				{
					'corp_id': corp.id,
					'product_ids': product_ids,
					'category_id': category_model.id
				}
			)

		return Category.from_model({
			"db_model": category_model
		})