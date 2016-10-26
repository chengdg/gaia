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
from business.common.filter_parser import FilterParser

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

	def __get_category_products_for_category_product_relations(self, product_relations):
		"""
		根据一批CategoryHasProduct model对象获取CategoryProduct对象集合
		"""
		product_ids = []
		product2relation = {}
		if product_relations:
			product_ids = [relation.product_id for relation in product_relations]
			product2relation.update(dict([(relation.product_id, relation) for relation in product_relations]))

		fill_options = {
			'with_price': True,
			'with_product_model': True,
			'with_shelve_status': True,
			'with_category': True
		}
		products = CorporationFactory.get().product_pool.get_products_by_ids(product_ids, fill_options)
		category_products = []
		for product in products:
			category_product = CategoryProduct(product)
			category_product.set_display_index(product2relation[product.id].display_index)
			category_products.append(category_product)

		return category_products


	def get_top_n_products(self, n):
		"""
		获得排序靠前的n个商品
		"""
		if n == UNLIMITED:
			product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=self.category.id).order_by(mall_models.CategoryHasProduct.display_index)
		else:
			product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=self.category.id).order_by(mall_models.CategoryHasProduct.display_index)[:n]

		category_products = self.__get_category_products_for_category_product_relations(product_relations)

		return category_products

	def get_products(self, target_page):
		"""
		获得商品分组中的商品集合
		"""
		#获得目标商品id集合
		product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=self.category.id).order_by(mall_models.CategoryHasProduct.display_index)
		pageinfo, product_relations = paginator.paginate(product_relations, target_page.cur_page, target_page.count_per_page)

		category_products = self.__get_category_products_for_category_product_relations(product_relations)

		return category_products, pageinfo

	def get_candidate_products_for_category(self, category_id, target_page, filters=None):
		"""
		获得商品分组的候选商品集合
		"""
		#商品详情填充选项
		fill_options = {
			'with_price': True,
			'with_shelve_status': True
		}

		if category_id == '0' or category_id == 0:
			products, pageinfo = CorporationFactory().get().product_pool.get_products(target_page, fill_options, filters=filters)
		else:
			#获取category的可选商品
			product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=category_id)
			product_ids = [relation.product_id for relation in product_relations]

			enhanced_filters = {
				'__f-id-notin': product_ids
			}
			if filters:
				enhanced_filters.update(filters)
			products, pageinfo = CorporationFactory().get().product_pool.get_products(target_page, fill_options, filters=enhanced_filters)

		#创建CategoryProduct对象
		category_products = []
		for product in products:
			category_product = CategoryProduct(product)
			category_products.append(category_product)

		return category_products, pageinfo