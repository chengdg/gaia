# -*- utf-8 -*-
from datetime import datetime
from bdem import msgutil
from eaglet.utils.resource_client import Resource

from db.mall import models as mall_models
from business import model as business_model
from business.mall.product import Product

class ProductShelf(business_model.Model):
	__slots__ = (
		'owner_id',
		'topic_name',
		'status',
		'msg_name'
	)

	def __init__(self, owner_id, status):
		self.owner_id = owner_id
		self.topic_name = "test-topic"
		if status == 'onshelf':
			self.status = mall_models.PRODUCT_SHELVE_TYPE_ON
			self.msg_name = 'msg_onshelf_product'
		elif status == 'offshelf':
			self.status = mall_models.PRODUCT_SHELVE_TYPE_OFF
			self.msg_name = 'msg_offshelf_product'
		elif status == 'recycled':
			self.status = mall_models.PRODUCT_SHELVE_TYPE_RECYCLED
			self.msg_name = 'msg_recycled_product'
		elif status == 'delete':
			self.status = status
			self.msg_name = 'msg_delete_product'

	def add_products(self, product_ids):
		if not product_ids:
			return 500, {'msg': 'Product_ids not null!'}
		if self.status == mall_models.PRODUCT_SHELVE_TYPE_OFF:
			product_ids = self.__exclude_group_product_id(product_ids)

		mall_models.Product.update(
			shelve_type=self.status,
			display_index=0,
			update_time=datetime.now()
		).dj_where(id__in=product_ids, owner=self.owner_id).execute()

		self.__send_msg_to_topic(product_ids)

	def get_products(self):
		product_models = mall_models.Product.select().dj_where(owner=self.owner_id, shelve_type=self.status, is_deleted=False)
		products = [Product(model) for model in product_models]
		#TODO添加商品的具体信息，搜索符合条件的商品

		return products

	def delete_products(self, product_ids):
		mall_models.Product.update(
			display_index=0,
			is_delete=True
		).dj_where(id__in=product_ids, owner=self.owner_id).execute()

		self.__send_msg_to_topic(product_ids)

	def __exclude_group_product_id(self, product_ids):
		params = {'woid': self.owner_id, 'pids': '_'.join([str(id) for id in product_ids])}

		resp = Resource.use('marketapp_apiserver').get({
			'resource': 'group.group_buy_products',
			'data': params
		})
		if resp and resp['code'] == 200:
			data = resp['data']
			product_groups = data['pid2is_in_group_buy']
			group_product_ids = []
			for product_group in product_groups:
				if product_group['pid'] in product_ids and product_group["is_in_group_buy"]:
					product_ids.remove(product_group['pid'])
					group_product_ids.append(product_group['pid'])
		return product_ids

	def __send_msg_to_topic(self, product_ids):
		data = {
			'name': self.msg_name,
			"data": {
				"product_ids": product_ids
			}
		}
		msgutil.send_message(self.topic_name, self.msg_name, data)
