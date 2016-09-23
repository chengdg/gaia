# -*- coding: utf-8 -*-
"""
出货单
"""
from business import model as business_model
from eaglet.decorator import param_required

from business.mall.supplier import Supplier
from business.product.delivery_items_products import DeliveryItemsProducts


class DeliveryItem(business_model.Model):
	__slots__ = (
		'id',
		'bid',
		'origin_order_id',
		'products',
		'supplier_id'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.id = db_model.id
		self.bid = db_model.origin_order_id

		if db_model.origin_order_id > 0:
			self.origin_order_id = db_model.origin_order_id
		else:
			self.origin_order_id = self.id

		if db_model.supplier:
			self.supplier_id = db_model.supplier + 's'
		elif db_model.supplier_user_id:
			self.supplier_id = db_model.supplier_user_id + 'u'
		else:
			self.supplier_id = ''

		self.context['db_model'] = db_model

	@staticmethod
	@param_required(['models'])
	def from_models(args):
		db_models = args['models']
		fill_options = args['fill_options']

		delivery_items = [DeliveryItem(db_model) for db_model in db_models]
		if fill_options['with_products']:
			DeliveryItem.__fill_products(delivery_items)

		return delivery_items

	@staticmethod
	def __fill_supplier(delivery_items):
		pass
		# suppliers = Supplier.from_ids()

	@staticmethod
	def __fill_products(delivery_items):
		delivery_items_products = DeliveryItemsProducts.get_for_delivery_items(delivery_items)

		delivery_item_id2products = {}
		for product in delivery_items_products:
			if product.delivery_item_id in delivery_item_id2products:
				delivery_item_id2products[product.delivery_item_id].append(product)
			else:
				delivery_item_id2products[product.delivery_item_id] = [product]

		for delivery_item in delivery_items:
			delivery_item.products = delivery_item_id2products[delivery_item.id]

	def to_dict(self, *extras):

		result = business_model.Model.to_dict(self, *extras)
		if self.products:
			result['products'] = [product.to_dict() for product in self.products]

		return result
