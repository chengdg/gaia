# -*- coding: utf-8 -*-
"""
出货单
"""
from business import model as business_model
from eaglet.decorator import param_required

from business.mall.supplier import Supplier
from business.product.delivery_items_products import DeliveryItemsProducts
from db.mall import models as mall_models


class DeliveryItem(business_model.Model):
	__slots__ = (
		'id',
		'bid',
		'origin_order_id',
		'products',
		'supplier_id',
		'postage',
		'status',
		'express_company_name',
		'express_number',
		'leader_name',
		'created_at',

		'supplier_name',
		'refunding_info',
		'total_origin_product_price',
		'refund_info',
		'supplier_info'
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

		self.postage = db_model.postage

		self.status = db_model.status

		self.supplier_name = 'todo'  # todo 填充

		# 快递公司信息
		self.express_company_name = db_model.express_company_name,
		self.express_number = db_model.express_number,
		self.leader_name = db_model.leader_name,

		self.context['db_model'] = db_model

	@staticmethod
	@param_required(['models'])
	def from_models(args):
		db_models = args['models']
		fill_options = args['fill_options']

		delivery_items = [DeliveryItem(db_model) for db_model in db_models]

		delivery_item_ids = []
		for delivery_item in delivery_items:
			delivery_item_ids.append(delivery_item.id)
		if fill_options['with_products']:
			DeliveryItem.__fill_products(delivery_items)

		if fill_options['with_refunding_info']:
			DeliveryItem.__fill_refunding_info(delivery_items, delivery_item_ids)

		DeliveryItem.__fill_supplier(delivery_items, delivery_item_ids)

		return delivery_items

	# suppliers = Supplier.from_ids()

	@staticmethod
	def __fill_products(delivery_items):
		delivery_items_products = DeliveryItemsProducts.get_for_delivery_items(delivery_items=delivery_items,
		                                                                       with_premium_sale=True)

		delivery_item_id2products = {}
		for product in delivery_items_products:
			if product.delivery_item_id in delivery_item_id2products:
				delivery_item_id2products[product.delivery_item_id].append(product)
			else:
				delivery_item_id2products[product.delivery_item_id] = [product]

		for delivery_item in delivery_items:
			delivery_item.products = delivery_item_id2products[delivery_item.id]
			delivery_item.total_origin_product_price = sum([p.total_origin_price for p in delivery_item.products])

	def to_dict(self, *extras):

		result = business_model.Model.to_dict(self, *extras)
		if self.products:
			result['products'] = [product.to_dict() for product in self.products]

		return result

	@staticmethod
	def __fill_refunding_info(delivery_items, delivery_item_ids):
		refund_info_list = mall_models.OrderHasRefund.select().dj_where(delivery_item_id__in=delivery_item_ids)

		delivery_item_id2refund_info = {refund_info.delivery_item_id: refund_info for refund_info in refund_info_list}

		for delivery_item in delivery_items:
			refund_info = delivery_item_id2refund_info.get(delivery_item.id)
			if refund_info:
				delivery_item.refund_info = {
					'cash': refund_info.cash,
					'weizoom_card_money': refund_info.weizoom_card_money,
					'integral': refund_info.integral,
					'integral_money': refund_info.integral_money,
					'coupon_money': refund_info.coupon_money,
					'total': refund_info.total,
					'finished': refund_info.finished
				}
			else:
				delivery_item.refund_info = {
					'cash': 0,
					'weizoom_card_money': 0,
					'integral': 0,
					'integral_money': 0,
					'coupon_money': 0,
					'total': 0,
					'finished': False
				}

	@staticmethod
	def __fill_supplier(delivery_items, delivery_item_ids):
		# todo 性能优化
		for delivery_item in delivery_items:
			db_model = delivery_item.context['db_model']
			supplier = None
			if db_model.supplier_user_id:
				supplier = Supplier.from_id({
					'id': db_model.supplier_user_id,
					'type': 'user'
				})
			elif db_model.supplier:
				supplier = Supplier.from_id({
					'id': db_model.supplier_user_id,
					'type': 'supplier'
				})

			if supplier:
				delivery_item.supplier_info = {
					'name': supplier.name,
					'type': supplier.type
				}
			else:
				delivery_item.supplier_info = {

				}
