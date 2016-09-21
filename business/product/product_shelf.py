# -*- utf-8 -*-
from datetime import datetime
from bdem import msgutil
from eaglet.utils.resource_client import Resource
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model


class ProductShelf(business_model.Model):
	__slots__ = (
		'owner_id',
		'topic_name',
		'type',
		'msg_name'
	)

	def __init__(self, owner_id, type):
		self.owner_id = owner_id
		self.topic_name = "test-topic"
		if type == 'onshelf':
			self.type = mall_models.PRODUCT_SHELVE_TYPE_ON
		elif type == 'offshelf':
			self.type = mall_models.PRODUCT_SHELVE_TYPE_OFF

	@staticmethod
	@param_required(['owner_id', 'type'])
	def create(args):
		owner_id = args['owner_id']
		type = args['type']
		if type not in ('onshelf', 'offshelf'):
			return None
		else:
			return ProductShelf(owner_id, type)

	def add_products(self, product_ids):
		if not product_ids:
			return False
		product_ids = self.__exclude_group_product_id(product_ids)

		mall_models.Product.update(
			shelve_type=self.status,
			display_index=0,
			update_time=datetime.now()
		).dj_where(id__in=product_ids, owner=self.owner_id).execute()

		if self.type == mall_models.PRODUCT_SHELVE_TYPE_ON:
			self.msg_name = 'msg_onshelf_product'
		elif self.type == mall_models.PRODUCT_SHELVE_TYPE_OFF:
			self.msg_name = 'msg_offshelf_product'

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
