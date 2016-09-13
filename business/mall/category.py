# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator
from business.mall.product import Product


class Category(business_model.Model):
	"""
	商品分组
	"""
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'pric_url',
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
	def empty_category(model=None):
		category = Category(model)
		return category

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		category = Category(model)
		return category

	@staticmethod
	@param_required(['owner_id'])
	def get_categories(params):
		'''
		分组管理列表
		'''
		print params
		filter_params = {'owner': params['owner_id']}
		if params['category_ids']:
			filter_params.update({'id__in': params['category_ids']})

		categories = mall_models.ProductCategory.select().dj_where(**filter_params)
		if params['category_ids']:
			return [Category.from_model({'db_model': category}) for category in categories], None
		pageinfo, categories = paginator.paginate(categories, params['cur_page'], params[
												'count_per_page'], query_string=params.get('query_string', None))
		return [Category.from_model({'db_model': category}) for category in categories], pageinfo.to_dict()


	def update_category_property(self, category_id, actionProperty='name', update_params={}):
		if actionProperty == 'position':
			mall_models.CategoryHasProduct.update(display_index=update_params['display_index']).dj_where(product_id=update_params['product_id'], category_id=category_id).execute()
		if actionProperty == 'products':
			category = mall_models.ProductCategory.get(id=category_id)
			product_ids = [product_id.strip() for product_id in update_params['product_ids'].strip().split(',') if product_id]
			products = Product.from_ids({'product_ids': product_ids})
			for b_product in products:
				opt = {
					'product': b_product.context['db_model'],
					'category': category
				}
				mall_models.CategoryHasProduct.get_or_create(**opt)
			category.product_count += len(products)
			category.save()
		else:
			mall_models.ProductCategory.update(name=update_params['name']).dj_where(id=category_id).execute()

	@staticmethod
	@param_required(['category_id'])
	def from_id(args):
		'''
		获取单个分组信息
		'''
		category = mall_models.ProductCategory.select().dj_where(id=args[
			'category_id'])
		if category.first():
			return Category(category.first())
		else:
			return None

	def save(self, owner_id, name, products=None):
		opt = {
			'owner': owner_id,
			'name': name
		}
		# created is True or False
		# If an object is found, get_or_create() returns a tuple of that object and False.
		# If multiple objects are found, get_or_create raises MultipleObjectsReturned.
		# If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
		# try:
		category, created = mall_models.ProductCategory.get_or_create(**opt)
		if products:
			for b_product in products:
				opt = {
					'product': b_product.context['db_model'],
					'category': category
				}
				mall_models.CategoryHasProduct.get_or_create(**opt)
			category.product_count = len(products)
			category.save()
			# mall_models.ProductCategory.update(product_count=len(products)).dj_where(id=category.id).execute()
		return Category(category)

	def delete_from_id(self, category_id):
		'''
		删除指定分组
		'''
		category = mall_models.ProductCategory.get(id=category_id)
		b_category = Category.from_model({'db_model': category})
		if b_category.products:
			mall_models.CategoryHasProduct.delete().dj_where(category=category).execute()
		return category.delete_instance()

	def delete_product(self, category_id, product_id):
		"""
		删除指定分组中的商品
		"""
		mall_models.CategoryHasProduct.delete().dj_where(category_id=category_id, product_id=product_id).execute()
		self.context['db_model'].product_count = int(self.context['db_model'].product_count) - 1
		self.context['db_model'].save()

	@property
	def products(self):
		product_relations = mall_models.CategoryHasProduct.select(
		).dj_where(category=self.context['db_model'])
		if product_relations:
			product_ids = [
				relation.product_id for relation in product_relations]

			self.context['products'] = Product.from_ids(
				{'product_ids': product_ids})
			return self.context['products']
		else:
			return []

	@products.setter
	def products(self, value):
		self.context['products'] = value

	def create(self, owner_id, name, product_ids=None):
		if product_ids:
			product_ids = [product_id.strip() for product_id in product_ids.strip().split(',') if product_id]
			products = Product.from_ids({'product_ids': product_ids})
		else:
			products = product_ids
		return self.save(owner_id, name, products)
