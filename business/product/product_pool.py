# coding=utf-8
# -*- utf-8 -*-
from datetime import datetime

from eaglet.decorator import param_required
from eaglet.core import paginator

from bdem import msgutil
from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models
from zeus_conf import TOPIC
from fill_product_detail_service import FillProductDetailService
from business.mall.corporation_factory import CorporationFactory
from business.common.filter_parser import FilterParser

NEW_PRODUCT_DISPLAY_INDEX = 9999999

class ProductPool(business_model.Model):
	__slots__ = (
		'corp',
		'corp_id'
	)

	def __init__(self, corp):
		business_model.Model.__init__(self)
		self.corp = corp
		self.corp_id = corp.id

	@staticmethod
	@param_required(['corp'])
	def get_for_corp(args):
		"""
		获得corp对应的商品池
		@param args:
		@return:
		"""
		return ProductPool(args['corp'])

	def add_products(self, product_ids):
		"""
		添加商品到商品池
		"""
		for product_id in product_ids:
			mall_models.ProductPool.create(
				woid=self.corp_id,
				product_id=product_id,
				status=mall_models.PP_STATUS_ON_POOL,
				type=mall_models.PP_TYPE_CREATE,
				display_index=NEW_PRODUCT_DISPLAY_INDEX
			)
		return True

	def add_consignment_products(self, product_ids):
		"""
		添加代售商品到商品池
		"""

		for product_id in product_ids:
			mall_models.ProductPool.create(
				woid=self.corp_id,
				product_id=product_id,
				status=mall_models.PP_STATUS_ON,
				type=mall_models.PP_TYPE_SYNC,
				display_index=NEW_PRODUCT_DISPLAY_INDEX,
				sync_at=datetime.now()
			)
		return True

	def __split_filters(self, filters):
		"""
		分离商品搜索的条件，分为：
		1、商品池搜索条件
		2、商品基本信息搜索条件
		3、商品细节搜索条件
		"""
		product_pool_filter_values = {}
		product_db_filter_values = {}
		product_model_filter_values = {}
		product_category_filter_values = {}

		filter_parse_result = FilterParser.get().parse(filters)

		for filter_field_op, filter_value in filter_parse_result.items():
			#获得过滤的field
			items = filter_field_op.split('__')
			filter_field = items[0]

			#按表将filter分散到不同的list中
			filter_category = None
			if filter_field == 'status' or filter_field == 'id':
				filter_category = product_pool_filter_values
			elif filter_field == 'name' or filter_field == 'bar_code' or filter_field == 'created_at':
				filter_category = product_db_filter_values
			elif filter_field == 'price' or filter_field == 'stocks':
				filter_category = product_model_filter_values
			elif filter_field == 'category':
				filter_category = product_category_filter_values
			filter_category[filter_field_op] = filter_value

		#补充条件
		product_pool_filter_values['woid'] = CorporationFactory.get().id
		if not 'status' in product_pool_filter_values:
			product_pool_filter_values['status__not'] = mall_models.PP_STATUS_DELETE

		return product_pool_filter_values, product_db_filter_values, product_model_filter_values, product_category_filter_values

	def get_products(self, page_info, fill_options=None, options={}, filters={}):
		"""
		根据条件在商品池搜索商品
		@return:
		"""
		product_pool_filter_values, product_db_filter_values, product_model_filter_values, product_category_filter_values = self.__split_filters(filters)

		#在product_pool表中进行过滤
		if product_pool_filter_values:
			if 'order_by_display_index' in options:
				pool_product_models = mall_models.ProductPool.select().dj_where(**product_pool_filter_values).order_by(mall_models.ProductPool.display_index, mall_models.ProductPool.product_id)
			else:
				pool_product_models = mall_models.ProductPool.select().dj_where(**product_pool_filter_values)
		else:
			if 'order_by_display_index' in options:
				pool_product_models = mall_models.ProductPool.select().dj_where(status__not=mall_models.PP_STATUS_DELETE).order_by(mall_models.ProductPool.display_index, mall_models.ProductPool.product_id)
			else:
				pool_product_models = mall_models.ProductPool.select().dj_where(status__not=mall_models.PP_STATUS_DELETE)
		product_ids = [pool_product_model.product_id for pool_product_model in pool_product_models]
		product2poolmodel = dict([(pool_product_model.product_id, pool_product_model) for pool_product_model in pool_product_models])

		#在mall_product_model中进行过滤
		if product_model_filter_values:
			product_model_filter_values['product_id__in'] = product_ids
			product_model_models = mall_models.ProductModel.select().dj_where(**product_model_filter_values)
			product_ids = [model.product_id for model in product_model_models]

		#在mall_category_has_product中进行过滤
		if product_category_filter_values:
			product_category_filter_values['product_id__in'] = product_ids
			relations = mall_models.CategoryHasProduct.select().dj_where(**product_category_filter_values)
			product_ids = [relation.product_id for relation in relations]

		#在mall_product表中进行过滤
		if product_db_filter_values:
			product_db_filter_values['id__in'] = product_ids
			product_models = mall_models.Product.select().dj_where(**product_db_filter_values)
			pageinfo, product_models = paginator.paginate(product_models, page_info.cur_page, page_info.count_per_page)
			print product_db_filter_values
			raw_input()
		else:
			pageinfo, product_ids = paginator.paginate(product_ids, page_info.cur_page, page_info.count_per_page)
			product_models = mall_models.Product.select().dj_where(id__in=product_ids)

		products = [Product(model) for model in product_models]
		fill_product_detail_service = FillProductDetailService.get(self.corp)
		fill_product_detail_service.fill_detail(products, fill_options)

		#按照product_ids中id的顺序对products进行顺序调整
		id2product = dict([(product.id, product) for product in products])
		result = []
		for product_id in product_ids:
			product_id = int(product_id)
			#因为products中的结果是分页后的结果，所以并不是所有的product_id对应的商品都在products中，这里需要判断
			product = id2product.get(product_id, None)
			if product:
				pool_product_model = product2poolmodel[product.id]
				if pool_product_model.type == mall_models.PP_TYPE_SYNC:
					product.create_type = 'sync'
					product.sync_at = pool_product_model.sync_at
				else:
					product.create_type = 'create'
				result.append(product)
		return result, pageinfo

	def get_products_by_ids(self, product_ids, fill_options={}):
		"""
		根据商品id获得商品集合
		@param product_ids: 商品id集合
		@return:
		"""
		product_models = mall_models.Product.select().dj_where(id__in=product_ids)
		products = [Product(model) for model in product_models]

		fill_product_detail_service = FillProductDetailService.get(self.corp)
		fill_product_detail_service.fill_detail(products, fill_options)

		pool_products = mall_models.ProductPool.select().dj_where(product_id__in=product_ids)
		id2product = dict([(product.id, product) for product in products])
		for pool_product in pool_products:
			if pool_product.type == mall_models.PP_TYPE_SYNC:
				product.create_type = 'sync'
				product.sync_at = pool_product.sync_at
			else:
				product.create_type = 'create'

		#按照product_ids中id的顺序对products进行顺序调整
		id2product = dict([(product.id, product) for product in products])
		result = []
		for product_id in product_ids:
			product_id = int(product_id)
			result.append(id2product[product_id])
		return result

	def __compatible_delete_products(self, product_ids):
		#[compatibility]: 兼容老的apiserver，在apiserver升级到支持ProductPool，本函数应该删除
		mall_models.Product.update(is_deleted=True).dj_where(id__in=product_ids).execute()

	def delete_products(self, product_ids):
		"""
		从商品池删除商品
		@param product_ids:
		@return:
		"""
		if product_ids:
			mall_models.ProductPool.update(
				display_index=NEW_PRODUCT_DISPLAY_INDEX,
				status=mall_models.PP_STATUS_DELETE
			).dj_where(product_id__in=product_ids, woid=self.corp_id).execute()

			self.__compatible_delete_products(product_ids)

			topic_name = TOPIC['product']
			msg_name = 'delete_product_from_pool'
			data = {
				"product_ids": product_ids
			}
			msgutil.send_message(topic_name, msg_name, data)
		return True
