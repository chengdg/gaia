# coding=utf-8
# -*- utf-8 -*-
from eaglet.decorator import param_required

from bdem import msgutil
from business import model as business_model

from business.product.product import Product
from db.mall import models as mall_models
from zeus_conf import TOPIC
from core import paginator

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

	def __search_product(self, products, filter_values):
		# 具体实现商品搜索的功能
		if filter_values:
			pass
		return products

	def __init__filter_values(self, filter_values):
		"""
		解析商品池搜索的条件
		@param filter_values:
		@return:
		"""
		product_pool_filter_values, product_db_filter_values, product_detail_filter_values = {}, {}, {}
		if 'status' in filter_values:
			product_pool_filter_values['status'] = filter_values['status']

		return product_pool_filter_values, product_db_filter_values, product_detail_filter_values

	def add_products(self, product_ids):
		"""
		添加商品到商品池
		@param product_ids:
		@return:
		"""
		for product_id in product_ids:
			mall_models.ProductPool.create(
				woid=self.corp_id,
				product_id=product_id,
				status=mall_models.PP_STATUS_ON_POOL
			)
		return True

	def get_products(self, filter_values, page_info):
		"""
		根据条件在商品池搜索商品
		@param filter_values:
		@return:
		"""
		product_pool_filter_values, product_db_filter_values, product_detail_filter_values = self.__init__filter_values(filter_values)

		product_ids = [model.product_id for model in mall_models.ProductPool.select().dj_where(**product_pool_filter_values)]
		product_db_filter_values['id__in'] = product_ids
		product_models = mall_models.Product.select().dj_where(**product_db_filter_values)
		pageinfo, product_models = paginator.paginate(product_models, page_info.cur_page, page_info.count_per_page)
		products = [Product.from_model({'model':model}) for model in product_models]
		if product_detail_filter_values:
			products = self.__search_product(products, product_detail_filter_values)
		return products, pageinfo

	def delete_products(self, product_ids):
		"""
		从商品池删除商品
		@param product_ids:
		@return:
		"""
		if product_ids:
			mall_models.ProductPool.update(
				display_index=0,
				status=mall_models.PP_STATUS_DELETE
			).dj_where(product_id__in=product_ids, owner=self.corp_id).execute()

			topic_name = TOPIC['product']
			msg_name = 'delete_product_from_pool'
			data = {
				"product_ids": product_ids
			}
			msgutil.send_message(topic_name, msg_name, data)
		return True
