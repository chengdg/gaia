# coding=utf-8
# -*- utf-8 -*-
from bdem import msgutil
from datetime import datetime
from eaglet.utils.resource_client import Resource
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model
from gaia_conf import TOPIC
from product_pool import ProductPool, NEW_PRODUCT_DISPLAY_INDEX

NEW_PRODUCT_DISPLAY_INDEX = 9999999

class ProductShelfError(Exception):
	def __init__(self, err_msg):
		self.err_msg = err_msg


class ProductShelf(business_model.Model):
	__slots__ = (
		'corp',
		'type'
	)

	def __init__(self, corp, type):
		self.corp = corp
		self.type = type

	@staticmethod
	@param_required(['corp', 'type'])
	def get(args):
		"""
		工厂方法：获得一个商品货架对象
		@param args:
		@return:
		"""
		corp = args['corp']
		type = args['type']
		if type in ('in_sale', 'for_sale'):
			return ProductShelf(corp, type)
		else:
			raise ProductShelfError('Product Shelf Type Error!')

	def __compatible_change_product_shelve_type(self, product_ids):
		#[compatibility]：兼容老的apiserver，在apiserver升级到支持ProductPool，下面的代码应该删除
			if self.type == 'in_sale':
				shelve_type = mall_models.PRODUCT_SHELVE_TYPE_ON
			elif self.type == 'for_sale':
				shelve_type = mall_models.PRODUCT_SHELVE_TYPE_OFF
			mall_models.Product.update(shelve_type=shelve_type).dj_where(id__in=product_ids).execute()

	def add_products(self, product_ids):
		"""
		在货架上添加商品
		@param product_ids:
		@return:
		"""
		if product_ids:
			if self.type == 'in_sale':
				msg_name = 'add_product_to_in_sale_shelf'
				product_shelf_type = mall_models.PP_STATUS_ON
			elif self.type == 'for_sale':
				msg_name = 'add_product_to_for_sale_shelf'
				product_shelf_type = mall_models.PP_STATUS_OFF

			mall_models.ProductPool.update(
				status=product_shelf_type,
				display_index=NEW_PRODUCT_DISPLAY_INDEX
			).dj_where(product_id__in=product_ids, woid=self.corp.id, status__gt=mall_models.PP_STATUS_DELETE).execute()
			
			if self.type == 'in_sale':
				#更新上架时间为加入"在售"货架的时间
				mall_models.ProductPool.update(sync_at=datetime.now()).dj_where(product_id__in=product_ids, woid=self.corp.id, status=product_shelf_type, sync_at=None).execute()

			self.__compatible_change_product_shelve_type(product_ids)
			# 上下架消息
			self.__send_msg_to_topic(product_ids, msg_name)
		return product_ids

	def move_products(self, product_ids):
		"""
		货架之间移动商品
		@param product_ids:
		@return:
		"""
		product_ids = self.__exclude_not_move_product_id(product_ids)
		if product_ids:
			product_ids = self.add_products(product_ids)
		return product_ids

	def get_products(self, page_info):
		"""
		获得货架上的商品集合
		"""
		return self.search_products({}, page_info)

	def search_products(self, filters, page_info):
		"""
		获得货架上的商品集合
		"""
		product_pool = self.corp.product_pool
		filters['__f-status-equal'] = mall_models.PP_STATUS_ON if self.type == 'in_sale' else mall_models.PP_STATUS_OFF

		fill_options = {
			'with_category': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_shelve_status': True,
			'with_supplier_info': True,
			'with_classification': True,
			'with_sales': True,
			'with_cps_promotion_info': True,
		}

		if self.type == 'in_sale':
			options = {
				'order_options': ['display_index', '-onshelf_time', '-id']
			}
		else:
			options = {
				'order_options': ['-id']
			}

		products, pageinfo = product_pool.get_products(page_info, fill_options, options, filters)

		return products, pageinfo

	def __exclude_not_move_product_id(self, product_ids):
		"""
		过滤不能移动的商品
		@param product_ids:
		@return:
		"""
		return product_ids
		#TODO: 连接团购api service
		# params = {'woid': self.corp.id, 'pids': '_'.join([str(id) for id in product_ids])}

		# resp = Resource.use('marketapp_apiserver').get({
		# 	'resource': 'group.group_buy_products',
		# 	'data': params
		# })
		# if resp and resp['code'] == 200:
		# 	data = resp['data']
		# 	product_groups = data['pid2is_in_group_buy']
		# 	group_product_ids = []
		# 	for product_group in product_groups:
		# 		if product_group['pid'] in product_ids and product_group["is_in_group_buy"]:
		# 			product_ids.remove(product_group['pid'])
		# 			group_product_ids.append(product_group['pid'])
		# return product_ids

	def __send_msg_to_topic(self, product_ids, msg_name):
		topic_name = TOPIC['product']
		data = {
			"product_ids": product_ids,
			"corp_id": self.corp.id
		}
		msgutil.send_message(topic_name, msg_name, data)

	def delete_products(self, product_ids):
		"""
		从货架上删除商品(放入商品池)
		"""
		product_pool = self.corp.product_pool

		product_pool.restore_products(product_ids)

	def search_cps_promoted_products(self, filters, page_info):
		"""
		获得货架上的商品集合
		"""
		product_pool = self.corp.product_pool

		filters['__f-status-equal'] = mall_models.PP_STATUS_ON if self.type == 'in_sale' else mall_models.PP_STATUS_OFF
		filters['__f-promotion_status-equal'] = mall_models.PROMOTING
		fill_options = {
			'with_category': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_supplier_info': True,
			'with_classification': True,
			'with_image': True,
			'with_cps_promotion_info': True,
			'with_product_label': True,
		}

		options = {
			'order_options': ['display_index', '-id']
		}

		products, pageinfo = product_pool.get_products(page_info, fill_options, options, filters)

		return products, pageinfo
