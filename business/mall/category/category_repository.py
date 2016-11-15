# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from bdem import msgutil
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator
from business.common.page_info import PageInfo

from business.mall.category.category import Category
from business.common.filter_parser import FilterParser
from gaia_conf import TOPIC


class CategoryRepository(business_model.Service):
	"""
	商品分组
	"""
	__slots__ = ()

	def get_all_categories(self, target_page):
		categories = mall_models.ProductCategory.select().dj_where(owner_id=self.corp.id)
		pageinfo, categories = paginator.paginate(categories, target_page.cur_page, target_page.count_per_page)

		return [Category.from_model({'db_model': category}) for category in categories], pageinfo

	def search_categories(self, filters, target_page):
		"""
		搜索商品分组
		"""
		pageinfo = None
		result_categories = None
		if '__f-product_name-contain' in filters:
			product_filters = FilterParser.get().extract_by_keys(filters, {
				'__f-product_name-contain': '__f-name-contain'
			})
			max_page = PageInfo.get_max_page()
			products, _ = self.corp.product_pool.get_products(max_page, filters=product_filters)
			product_ids = [product.id for product in products]
			category_ids = [relation.category_id for relation in mall_models.CategoryHasProduct.select().dj_where(product_id__in=product_ids)]
			result_categories = mall_models.ProductCategory.select().dj_where(id__in=category_ids)
			pageinfo, result_categories = paginator.paginate(result_categories, target_page.cur_page, target_page.count_per_page)

		if '__f-name-contain' in filters:
			filter_parse_result = FilterParser.get().parse_key(filters, '__f-name-contain')
			params = {
				"owner_id": self.corp.id,
			}
			params.update(filter_parse_result)
			categories = mall_models.ProductCategory.select().dj_where(**params)
			if result_categories:
				#搜索场景：同时搜索“分组名”和“分组商品名”，基本不常用
				#这里分页的逻辑非常复杂，所以，这种情况暂不支持分页
				category_id_set = [category.id for category in categories]
				result_categories = [category for category in result_categories if category.id in category_id_set]
			else:
				pageinfo, result_categories = paginator.paginate(categories, target_page.cur_page, target_page.count_per_page)

		return [Category.from_model({'db_model': category}) for category in result_categories], pageinfo

	def get_categories_by_ids(self, category_ids):
		categories = mall_models.ProductCategory.select().dj_where(id__in=category_ids)
		return [Category.from_model({'db_model': category}) for category in categories]

	def get_category(self, category_id):
		"""
		获得指定的category
		"""
		return self.get_categories_by_ids([category_id])[0]

	def delete_category(self, category_id):
		mall_models.CategoryHasProduct.delete().dj_where(category=category_id).execute()
		mall_models.ProductCategory.delete().dj_where(owner_id=self.corp.id, id=category_id).execute()
		msgutil.send_message(TOPIC['product'], 'category_deleted', {'category_id': category_id, 'corp_id': self.corp.id})

	def delete_products_in_categories(self, product_ids):
		"""
		从corp的所有分类中都删除product_ids中指定的商品
		"""
		categories = mall_models.ProductCategory.select().dj_where(owner_id=self.corp.id)
		category_ids = [category.id for category in categories]
		mall_models.CategoryHasProduct.delete().dj_where(product_id__in=product_ids, category_id__in=category_ids).execute()

		for category_id in category_ids:
			Category.update_product_count(category_id)
