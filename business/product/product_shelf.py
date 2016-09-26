# coding=utf-8
# -*- utf-8 -*-
from bdem import msgutil
from eaglet.utils.resource_client import Resource
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model
from zeus_conf import TOPIC
from product_pool import ProductPool

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
				display_index=0
			).dj_where(product_id__in=product_ids, woid=self.corp.id, status__gt=mall_models.PP_STATUS_DELETE).execute()

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
		product_pool = self.corp.product_pool
		#TODO: get_products不应泄露DB层信息
		if self.type == 'in_sale':
			query = {
				"status": mall_models.PP_STATUS_ON
			}
		else:
			query = {
				"status": mall_models.PP_STATUS_OFF
			}

		products, pageinfo = product_pool.get_products(query, page_info)

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
			"product_ids": product_ids
		}
		msgutil.send_message(topic_name, msg_name, data)