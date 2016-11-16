# coding=utf-8
# -*- utf-8 -*-
from datetime import datetime

from eaglet.decorator import param_required
from eaglet.core import paginator

from bdem import msgutil
from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models
from gaia_conf import TOPIC
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
				status=mall_models.PP_STATUS_ON_POOL,
				type=mall_models.PP_TYPE_SYNC,
				display_index=NEW_PRODUCT_DISPLAY_INDEX,
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
		product_sales_filter_values = {}
		product_supplier_filter_values = {}
		product_classification_filter_values = {}
		product_promotion_filter_values = {}
		product_label_filter_values = {}

		filter_parse_result = FilterParser.get().parse(filters)
		should_add_default_status = True #是否添加默认的商品status条件
		# 是否添加规格信息的is_deleted字段
		should_add_default_model_is_deleted = True
		for filter_field_op, filter_value in filter_parse_result.items():
			#获得过滤的field
			items = filter_field_op.split('__')
			filter_field = items[0]
			op = None
			if len(items) > 1:
				op = items[1]

			#按表将filter分散到不同的list中
			filter_category = None
			should_ignore_field = False #是否略过该field不处理
			if filter_field == 'id':
				filter_field = 'product_id'
				filter_field_op = 'product_id'
				filter_category = product_pool_filter_values
			elif filter_field == 'status':
				should_add_default_status = False
				filter_category = product_pool_filter_values
			elif filter_field == 'sync_at':
				filter_category = product_pool_filter_values
			elif filter_field == 'name' or filter_field == 'bar_code' or filter_field == 'created_at':
				filter_category = product_db_filter_values
			elif filter_field == 'price' or filter_field == 'stocks':
				filter_category = product_model_filter_values
				should_add_default_model_is_deleted = True
			elif filter_field == 'category':
				filter_category = product_category_filter_values
			elif filter_field == 'sales':
				filter_category = product_sales_filter_values
			elif filter_field == 'supplier_type':
				filter_field_op = 'type'
				filter_category = product_supplier_filter_values
				if filter_value == 'fixed':
					filter_value = mall_models.SUPPLIER_TYPE_FIXED
				elif filter_value == 'divide':
					filter_value = mall_models.SUPPLIER_TYPE_DIVIDE
				elif filter_value == 'retail':
					filter_value = mall_models.SUPPLIER_TYPE_RETAIL
			elif filter_field == 'supplier':
				filter_field_op = 'name__icontains'
				op = None
				filter_category = product_supplier_filter_values
			elif filter_field == 'secondary_classification':
				child_category_ids = [child.id for child in self.corp.product_classification_repository.get_children_product_classifications(filter_value)]
				filter_field_op = 'classification_id__in'
				filter_value = child_category_ids
				filter_category = product_classification_filter_values
			elif filter_field == 'first_classification':
				if not 'secondary_classification' in filter_parse_result:
					child_category_ids = [child.id for child in self.corp.product_classification_repository.get_children_product_classifications(filter_value)]
					filter_field_op = 'classification_id__in'
					filter_value = child_category_ids
					filter_category = product_classification_filter_values
				else:
					should_ignore_field = True
			elif filter_field == 'promotion_status':
				filter_field_op = 'promote_status'
				filter_category = product_promotion_filter_values
			elif filter_field == 'labels':
				filter_category = product_label_filter_values
				filter_field = 'label_id'

			if not should_ignore_field:
				if op:
					filter_field_op = '%s__%s' % (filter_field, op)
				filter_category[filter_field_op] = filter_value

		#补充条件
		product_pool_filter_values['woid'] = CorporationFactory.get().id
		if should_add_default_status:
			product_pool_filter_values['status__not'] = mall_models.PP_STATUS_DELETE

		if should_add_default_model_is_deleted:
			product_model_filter_values['is_deleted'] = False

		return {
			'product_pool': product_pool_filter_values,
			'product_info': product_db_filter_values,
			'product_model': product_model_filter_values,
			'product_category': product_category_filter_values,
			'product_sales': product_sales_filter_values,
			'product_supplier': product_supplier_filter_values,
			'product_classification': product_classification_filter_values,
			'product_promotion': product_promotion_filter_values,
			'product_label': product_label_filter_values
		}

	def __get_product_order_fields(self, options):
		"""
		获得商品排序field集合
		"""
		options = {} if not options else options
		type2field = {
			'display_index': mall_models.ProductPool.display_index,
			'status': mall_models.ProductPool.status,
			'onshelf_time': mall_models.ProductPool.sync_at,
			'id': mall_models.ProductPool.product_id
		}

		fields = []
		for order_type in options.get('order_options', []):
			is_desc = False
			if order_type[0] == '-':
				is_desc = True
				order_type = order_type[1:]

			field = type2field[order_type]
			if is_desc:
				field = field.desc()

			fields.append(field)

		return fields

	def get_products(self, page_info, fill_options=None, options=None, filters=None):
		"""
		根据条件在商品池搜索商品
		@return:
		"""
		type2filters = self.__split_filters(filters)

		#构建排序策略
		order_fields = self.__get_product_order_fields(options)

		#在product_pool表中进行过滤
		product_pool_filters = type2filters['product_pool']
		#进行查询
		if product_pool_filters:
			# 补充首次上架时间搜索值null判断
			sync_at__range = product_pool_filters.get('sync_at__range')
			if sync_at__range:
				sync_at__range = list(sync_at__range)
				if not sync_at__range[0]:
					sync_at__range[0] = '1999-01-01'
				if not sync_at__range[1]:
					sync_at__range[1] = '2999-01-01'
				product_pool_filters['sync_at__range'] = sync_at__range
			pool_product_models = mall_models.ProductPool.select().dj_where(**product_pool_filters)			
		else:
			pool_product_models = mall_models.ProductPool.select().dj_where(status__not=mall_models.PP_STATUS_DELETE)			
		if len(order_fields) > 0:
			pool_product_models = pool_product_models.order_by(*order_fields)

		#获取查询结果
		product_ids = [pool_product_model.product_id for pool_product_model in pool_product_models]
		product2poolmodel = dict([(pool_product_model.product_id, pool_product_model) for pool_product_model in pool_product_models])

		#在mall_product_model中进行过滤
		product_model_filters = type2filters['product_model']
		if product_model_filters:
			product_model_filters['product_id__in'] = product_ids
			# 只设置库存最小值，不设置库存最大值的情况下，才能将库存为无限的商品查询出来
			stocks__lte = product_model_filters.get('stocks__lte')
			if stocks__lte and stocks__lte != u'999999999':
				product_model_filters['stock_type'] = mall_models.PRODUCT_STOCK_TYPE_LIMIT

			product_model_models = mall_models.ProductModel.select().dj_where(**product_model_filters)
			product_ids = [model.product_id for model in product_model_models]
			product_ids = list(set(product_ids))

		#在mall_category_has_product中进行过滤
		product_category_filters = type2filters['product_category']
		if product_category_filters:
			product_category_filters['product_id__in'] = product_ids
			relations = mall_models.CategoryHasProduct.select().dj_where(**product_category_filters)
			product_ids = [relation.product_id for relation in relations]

		#在mall_product_sales中进行过滤
		product_sales_filters = type2filters['product_sales']
		if product_sales_filters:
			product_sales_filters['product_id__in'] = product_ids
			models = mall_models.ProductSales.select().dj_where(**product_sales_filters)
			sales__lte = product_sales_filters.get('sales__lte')
			sales__gte = product_sales_filters.get('sales__gte')
			# 不在mall_product_sales 的product
			temp_product_ids = []
			# 在mall_product_sales中没有数据的商品销量也是0
			if int(sales__gte) <= 0 and int(sales__lte) >= 0:
				all_product_sales_models = mall_models.ProductSales.select().dj_where(product_id__in=product_ids)
				all_product_ids = [sales_model.product_id for sales_model in all_product_sales_models]

				temp_product_ids = list(set(product_ids) - set(all_product_ids))

			product_ids = [model.product_id for model in models]
			if temp_product_ids:
				product_ids += temp_product_ids

		#根据供应商进行过滤
		product_supplier_filters = type2filters['product_supplier']
		supplier_ids = None
		if product_supplier_filters:
			supplier_ids = [supplier.id for supplier in mall_models.Supplier.select().dj_where(**product_supplier_filters)]

		#根据商品分类进行过滤
		product_classification_filters = type2filters['product_classification']
		if product_classification_filters:
			product_classification_filters['product_id__in'] = product_ids
			product_ids = [relation.product_id for relation in mall_models.ClassificationHasProduct.select().dj_where(**product_classification_filters)]

		#根据商品标签进行过滤
		product_label_filters = type2filters['product_label']
		if product_label_filters:
			product_label_filters['product_id__in'] = product_ids
			product_ids = [relation.product_id for relation in mall_models.ProductHasLabel.select().dj_where(**product_label_filters)]

		# 根据cps推广进行过滤
		product_promotion_filter_values = type2filters['product_promotion']
		if product_promotion_filter_values:
			if product_ids:
				product_promotion_filter_values.update({'product_id__in': product_ids})
				product_ids = [promote.product_id for promote in mall_models.PromoteDetail.select().dj_where(**product_promotion_filter_values)]
				# product_ids = list(set(product_ids) - set(promoted_product_ids))

		#在mall_product表中进行过滤
		product_info_filters = type2filters['product_info']
		if supplier_ids:
			product_info_filters['supplier_id__in'] = supplier_ids
		if product_info_filters:
			product_info_filters['id__in'] = product_ids
			product_models = mall_models.Product.select().dj_where(**product_info_filters)
			pageinfo, product_models = paginator.paginate(product_models, page_info.cur_page, page_info.count_per_page)
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
				else:
					product.create_type = 'create'
				product.sync_at = pool_product_model.sync_at
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

	def get_product_by_id(self, product_id, fill_options={}):
		return self.get_products_by_ids([product_id], fill_options=fill_options)[0]

	def __compatible_delete_products(self, product_ids):
		#[compatibility]: 兼容老的apiserver，在apiserver升级到支持ProductPool，本函数应该删除

		# if self.corp.type == 'normal':
		# 在当前阶段，只有自建商品执行此删除
		mall_models.Product.update(is_deleted=True).dj_where(id__in=product_ids,
															 owner_id=self.corp.id).execute()

	def delete_products(self, product_ids):
		"""
		从商品池删除商品
		@param product_ids:
		@return:
		"""
		if product_ids:
			#在product pool中删除
			mall_models.ProductPool.update(
				display_index=NEW_PRODUCT_DISPLAY_INDEX,
				status=mall_models.PP_STATUS_DELETE
			).dj_where(product_id__in=product_ids, woid=self.corp_id).execute()

			#从分组中删除
			self.corp.category_repository.delete_products_in_categories(product_ids)

			#对于代销商品，重新将其放回商品池
			mall_models.ProductPool.update(
				status=mall_models.PP_STATUS_ON_POOL
			).dj_where(product_id__in=product_ids, woid=self.corp_id, type=mall_models.PP_TYPE_SYNC).execute()

			self.__compatible_delete_products(product_ids)

			topic_name = TOPIC['product']
			msg_name = 'product_deleted'
			data = {
				"corp_id": self.corp.id,
				"product_ids": product_ids
			}
			msgutil.send_message(topic_name, msg_name, data)
		return True

	def restore_products(self, product_ids):
		"""
		将商品放回到商品池中
		"""
		if product_ids:
			mall_models.ProductPool.update(
				display_index=NEW_PRODUCT_DISPLAY_INDEX,
				status=mall_models.PP_STATUS_ON_POOL
			).dj_where(product_id__in=product_ids, woid=self.corp.id).execute()

			#从分组中删除
			self.corp.category_repository.delete_products_in_categories(product_ids)

			topic_name = TOPIC['product']
			msg_name = 'product_deleted'
			data = {
				"corp_id": self.corp.id,
				"product_ids": product_ids
			}
			msgutil.send_message(topic_name, msg_name, data)

	def search_promoted_products(self, filters, page_info):
		product_pool = self.corp.product_pool

		filters['__f-status-equal'] = mall_models.PP_STATUS_ON_POOL
		filters['__f-promotion_status-equal'] = mall_models.PROMOTING
		fill_options = {
			'with_category': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_shelve_status': True,
			'with_supplier_info': True,
			'with_classification': True,
			'with_sales': True,
			'with_cps_promotion_info': True
		}

		options = {
			'order_options': ['display_index', '-id']
		}

		products, pageinfo = product_pool.get_products(page_info, fill_options, options, filters)

		return products, pageinfo

	def get_unprocessed_cps_promoted_products_count(self):
		"""

		"""

		new_promoted_product = mall_models.PromoteDetail.select().dj_where(is_new=True,
																		   promote_status=mall_models.PROMOTING)
		promoting_product_ids = [promoted_product.product_id for promoted_product in new_promoted_product]
		pool_product_models = mall_models.ProductPool.select().dj_where(status__in=[mall_models.PP_STATUS_ON_POOL,
																					mall_models.PP_STATUS_ON,
																					mall_models.PP_STATUS_OFF],
																		woid=self.corp.id,
																		is_cps_promotion_processed=False,
																		product_id__in=promoting_product_ids)

		return pool_product_models.count()

	def set_cps_promoted_products_processed(self, product_ids):

		mall_models.ProductPool.update(is_cps_promotion_processed=True)\
			.dj_where(product_id__in=product_ids,
					  woid=self.corp.id).execute()
