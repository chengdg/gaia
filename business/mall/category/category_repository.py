# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator
from business.common.page_info import PageInfo

from business.mall.category.category import Category

class CategoryRepository(business_model.Service):
	"""
	商品分组
	"""
	__slots__ = ()

	def get_all_categories(self, target_page):
		categories = mall_models.ProductCategory.select().dj_where(owner_id=self.corp.id)
		pageinfo, categories = paginator.paginate(categories, target_page.cur_page, target_page.count_per_page)
		return [Category.from_model({'db_model': category}) for category in categories], pageinfo

	def get_specific_categories(self, category_ids):
		categories = mall_models.ProductCategory.select().dj_where(id__in=category_ids)
		return [Category.from_model({'db_model': category}) for category in categories]

	def delete_category(self, category_id):
		mall_models.CategoryHasProduct.delete().dj_where(category=category_id).execute()
		mall_models.ProductCategory.delete().dj_where(owner_id=self.corp.id, id=category_id).execute()