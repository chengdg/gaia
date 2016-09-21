# -*- utf-8 -*-
from eaglet.decorator import param_required

from bdem import msgutil
from business import model as business_model

from business.mall.product import Product
from db.mall import models as mall_models

class ProductPool(business_model.Model):
	__slots__ = (
		'owner_id'
	)

	def __init__(self, owner_id):
		business_model.Model.__init__(self)
		self.owner_id = owner_id

	@staticmethod
	@param_required(['owner_id'])
	def from_owner_id(args):
		owner_id = args['owner_id']
		return ProductPool(owner_id)

	def __seach_product(self, products, filter_values):
		# 具体实现商品搜索的功能
		if not filter_values:
			return products
		return products

	def __init__filter_values(self, filter_values):
		return filter_values

	def get_product(self, filter_values):
		filter_values = self.__init__filter_values(filter_values)
		product_models = mall_models.Product.select().dj_where(owner=self.owner_id, is_deleted=False)
		products = [Product(model) for model in product_models]
		products = self.__seach_product(products, filter_values)
		return products

	def delete_products(self, product_ids):
		if not product_ids:
			return False
		mall_models.Product.update(
			display_index=0,
			is_delete=True
		).dj_where(id__in=product_ids, owner=self.owner_id).execute()

		topic_name = 'test-topic'
		msg_name = 'msg_delete_product'
		data = {
			'name': "delete_product",
			"data": {
				"product_ids": product_ids
			}
		}
		msgutil.send_message(topic_name, msg_name, data)
		return True
