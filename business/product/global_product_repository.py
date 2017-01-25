# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from db.mall import models as mall_models
from product import Product

class GlobalProductRepository(business_model.Service):
	FILTER_CONST = {
		'ALL': -1, #全部
		'NOT_YET': 0, #未审核
		'SUBMIT': 1, #审核中
		'PASSED': 2, #审核通过
		'POOL_REFUSED': 3, #入库驳回
		'UPDATE_REFUSED': 4 #修改驳回
	}

	def __fill_product_details(self, products, fill_options):
		from business.product.fill_product_detail_service import FillProductDetailService
		FillProductDetailService.get().fill_detail(products, fill_options)

	def __get_filter_params(self, args):
		params = {}
		for param in args:
			if not param.startswith('__f-'):
				continue
			_, field, __ = param.split('-')
			params[field] = args[param]
		return params

	def filter_products(self, query_dict, page_info, fill_options=None):
		db_models = mall_models.Product.select().dj_where(is_deleted=False)

		if query_dict['corp'].is_weizoom_corp():
			db_models = db_models.where(
				(mall_models.Product.status << [mall_models.PRODUCT_STATUS['SUBMIT'], mall_models.PRODUCT_STATUS['REFUSED']])
				| (mall_models.Product.is_accepted == True)
			)
		else:
			db_models = db_models.dj_where(owner_id=query_dict['corp'].id)

		#筛选
		filter = self.__get_filter_params(query_dict)
		product_name = filter.get('name')
		classification_name = filter.get('classification')
		status = filter.get('status')
		owner_name = filter.get('owner_name')

		if product_name:
			db_models = db_models.dj_where(name__icontains=product_name)
		if classification_name:
			classification_models = mall_models.Classification.select().dj_where(name__icontains=classification_name)
			relation_models = mall_models.ClassificationHasProduct.select().dj_where(classification_id__in=[c.id for c in classification_models])
			db_models = db_models.dj_where(id__in=[r.product_id for r in relation_models])
		if not status == None or (not int(status) == self.FILTER_CONST['ALL']):
			status = int(status)
			if status in [self.FILTER_CONST['NOT_YET'], self.FILTER_CONST['SUBMIT']]:
				db_models = db_models.dj_where(status=status)
			elif status == self.FILTER_CONST['POOL_REFUSED']:
				db_models = db_models.dj_where(status=mall_models.PRODUCT_STATUS['REFUSED'], is_accepted=False)
			elif status == self.FILTER_CONST['UPDATE_REFUSED']:
				db_models = db_models.dj_where(status=mall_models.PRODUCT_STATUS['REFUSED'], is_accepted=True, is_updated=True)
			elif status == self.FILTER_CONST['PASSED']:
				db_models = db_models.dj_where(status=mall_models.PRODUCT_STATUS['NOT_YET'], is_accepted=True)

		if owner_name:
			#TODO
			pass

		if page_info:
			pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)
		else:
			pageinfo = None

		products = []
		for model in db_models:
			pre_product = Product(model)
			products.append(pre_product)

		fill_options = fill_options if fill_options else {}
		self.__fill_product_details(products, fill_options)

		return pageinfo, products

	def get_product(self, product_id, fill_options=None):
		db_model = mall_models.Product.select().dj_where(id=product_id, is_deleted=False).get()
		product = Product(db_model)
		self.__fill_product_details([product], fill_options)
		return product

	def get_products_by_ids(self, product_ids, fill_options=None):
		product_models = mall_models.Product.select().dj_where(id__in=product_ids)
		products = [Product(model) for model in product_models]

		self.__fill_product_details(products, fill_options)

		pool_products = mall_models.ProductPool.select().dj_where(product_id__in=product_ids)
		id2product = dict([(product.id, product) for product in products])
		for pool_product in pool_products:
			product = id2product[pool_product.product_id]
			if pool_product.type == mall_models.PP_TYPE_SYNC:
				product.create_type = 'sync'
				product.sync_at = pool_product.sync_at
			else:
				product.create_type = 'create'

		# 按照product_ids中id的顺序对products进行顺序调整
		result = []
		for product_id in product_ids:
			product_id = int(product_id)
			result.append(id2product[product_id])
		return result