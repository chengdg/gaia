# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator
from eaglet.core.db import models as eaglet_db

from business.product.product import Product
from business.mall.corporation_factory import CorporationFactory
from business.mall.category.category_product import CategoryProduct
from business.common.filter_parser import FilterParser

UNLIMITED = -1

class FakeObjects(object):
	def __init__(self):
		pass

	def __getitem__(self, key):
		return None

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
			'with_category': True,
			'with_sales': True
		}
		products = CorporationFactory.get().product_pool.get_products_by_ids(product_ids, fill_options)
		category_products = []
		for product in products:
			category_product = CategoryProduct(product)
			relation = product2relation[product.id]
			category_product.set_display_index(relation.display_index)
			category_product.set_created_at(relation.created_at)
			category_products.append(category_product)

		return category_products

	def get_top_n_products(self, n):
		"""
		获得排序靠前的n个商品
		"""
		from business.common.page_info import PageInfo

		if n == UNLIMITED:
			n = 9999

		target_page = PageInfo.create({
			"cur_page": 1,
			"count_per_page": n
		})

		category_products, _ = self.get_products(target_page)
		return category_products

	def get_products(self, target_page):
		"""
		获得category中的商品集合
		"""
		corp_id = int(CorporationFactory.get().id)

		#由于历史数据库设计不合理，导致sql语句太复杂，这里使用raw sql进行查询
		sql = """
		SELECT c.id as id, c.category_id as category_id, c.product_id as product_id, p.status as status, c.display_index as display_index 
		FROM mall_category_has_product as c INNER JOIN product_pool as p
		WHERE c.category_id = %d AND p.woid = %d AND c.product_id = p.product_id AND p.status in (0, 1) ORDER BY status desc, display_index, id desc
		LIMIT %d
		OFFSET %d
		""" % (self.category.id, corp_id, target_page.count_per_page, (target_page.cur_page-1)*target_page.count_per_page)

		db = eaglet_db.db
		cursor = db.execute_sql(sql, ())
		relation_ids = []
		product2index = {}
		for index, row in enumerate(cursor.fetchall()):
			relation_id = row[0]
			product_id = row[2]
			relation_ids.append(relation_id)
			product2index[product_id] = index
		
		product_relations = mall_models.CategoryHasProduct.select().dj_where(id__in=relation_ids)
		category_products = self.__get_category_products_for_category_product_relations(product_relations)
		
		objects = FakeObjects()
		objects.item_count = mall_models.CategoryHasProduct.select().dj_where(category_id=self.category.id).count()
		pageinfo, _ = paginator.paginate(objects, target_page.cur_page, target_page.count_per_page)

		category_products.sort(lambda x,y: cmp(product2index[x.id], product2index[y.id]))
		return category_products, pageinfo

	def get_candidate_products_for_category(self, category_id, target_page, filters=None):
		"""
		获得商品分组的候选商品集合
		"""
		#商品详情填充选项
		fill_options = {
			'with_price': True,
			'with_shelve_status': True,
			'with_sales': True
		}

		if filters is None:
			filters = {}
		filters['__f-status-in'] = [mall_models.PP_STATUS_OFF, mall_models.PP_STATUS_ON]

		options = {
			'order_options': ['-status', '-id']
		}

		if category_id == '0' or category_id == 0:
			products, pageinfo = CorporationFactory().get().product_pool.get_products(target_page, fill_options, filters=filters, options=options)
		else:
			#获取category的可选商品
			product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=category_id)
			product_ids = [relation.product_id for relation in product_relations]

			enhanced_filters = {
				'__f-id-notin': product_ids
			}
			if filters:
				enhanced_filters.update(filters)
			products, pageinfo = CorporationFactory().get().product_pool.get_products(target_page, fill_options, filters=enhanced_filters, options=options)

		#创建CategoryProduct对象
		category_products = []
		for product in products:
			category_product = CategoryProduct(product)
			category_products.append(category_product)

		return category_products, pageinfo
	
	
	def get_on_shelf_products_for_category(self, category_id, corp_id, fill_options=None, target_page=None):
		"""
		获取分组下的上架商品集合
		"""
		product_relations = mall_models.CategoryHasProduct.select().dj_where(category_id=category_id)\
			.order_by(mall_models.CategoryHasProduct.display_index, mall_models.CategoryHasProduct.created_at.desc())
		
		product_ids = [relation.product_id for relation in product_relations]
		on_shelf_products = mall_models.ProductPool.select().dj_where(product_id__in=product_ids,
																		 status=mall_models.PP_STATUS_ON,
																		 woid=corp_id)
		on_shelf_product_ids = []
		if not fill_options:
			
			products = []
			for pool in on_shelf_products:
				on_shelf_product_ids.append(pool.product_id)
				product = mall_models.Product()
				product.id = pool.product_id
				products.append(Product(product))
			products = sorted(products, key=lambda k: product_ids.index(k.product_id))
			page_info, products = paginator.paginate(products, target_page.cur_page, target_page.count_per_page)
			return products, page_info
		else:
			options = {
				'order_options': ['-status', '-id']
			}
			filters = {
				'__f-id-in': on_shelf_product_ids
			}
			products, pageinfo = CorporationFactory().get().product_pool.get_products(target_page, fill_options,
																					  filters=filters,
																					  options=options,)
			return products, pageinfo
