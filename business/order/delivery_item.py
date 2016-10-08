# -*- coding: utf-8 -*-
"""
出货单
"""
from business import model as business_model
from eaglet.decorator import param_required

from business.mall.supplier import Supplier
from business.product.delivery_items_products import DeliveryItemsProducts
from db.mall import models as mall_models
from db.express import models as express_models


class DeliveryItem(business_model.Model):
	__slots__ = (
		'id',
		'bid',
		'origin_order_id',
		'products',

		'postage',
		'status',
		'express_company_name',
		'express_number',
		'leader_name',
		'created_at',

		'refunding_info',
		'total_origin_product_price',
		'supplier_info',
		'express_details'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		self.id = db_model.id
		self.bid = db_model.order_id

		if db_model.origin_order_id > 0:
			self.origin_order_id = db_model.origin_order_id
		else:
			self.origin_order_id = db_model.id

		self.postage = db_model.postage

		self.status = db_model.status

		# 快递公司信息
		self.express_company_name = db_model.express_company_name
		self.express_number = db_model.express_number
		self.leader_name = db_model.leader_name
		self.created_at = db_model.created_at
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
		if fill_options.get('with_products'):
			DeliveryItem.__fill_products(delivery_items)

		if fill_options.get('with_refunding_info'):
			DeliveryItem.__fill_refunding_info(delivery_items, delivery_item_ids)

		if fill_options.get('with_express_details'):
			DeliveryItem.__fill_express_details(delivery_items, delivery_item_ids)

		DeliveryItem.__fill_supplier(delivery_items, delivery_item_ids)

		return delivery_items

	# suppliers = Supplier.from_ids()

	@staticmethod
	def __fill_express_details(delivery_items, delivery_item_ids):
		"""
		物流信息
		@param delivery_items:
		@param delivery_item_ids:
		@return:
		"""
		details =express_models.ExpressDetail.select().dj_where(order_id__in=delivery_item_ids).order_by('-display_index')
		other_delivery_items = []
		if details.count() > 0:
			# 兼容历史数据,老数据里订单的发货信息直接关联到ExpressDetail
			delivery_item_id2details = {}

			for detail in details:
				if detail.order_id in delivery_item_id2details:
					delivery_item_id2details[detail.order_id].append(detail)
				else:
					delivery_item_id2details[detail.order_id] = [detail]

			for delivery_item in delivery_items:
				express_details = delivery_item_id2details.get(delivery_item.id)
				if express_details:
					for detail in express_details:
						delivery_item.express_details.append({
							'ftime': detail.ftime,
							'context': detail.context
						})
				else:

					other_delivery_items.append(delivery_items)
		else:
			other_delivery_items = delivery_items
		if other_delivery_items:
			express_company_names = []
			express_numbers = []
			for delivery_item in delivery_items:
				express_company_names.append(delivery_item.express_company_name)
				express_numbers.append(delivery_item.express_number)

				delivery_item.express_details = []

			express_push_list = express_models.ExpressHasOrderPushStatus.select().dj_where(
				express_company_name__in=express_company_names,
				express_number__in=express_numbers
			)

			name_number2express_push_id = {str(push.express_company_name + '__' + push.express_number):push.id for push in express_push_list}

			express_push_ids = []
			for push in express_push_list:
				express_push_ids.append(push.id)

			express_details = express_models.ExpressDetail.select().dj_where(express_id__in=express_push_ids)
			express_push_id2details = {detail.express_id:detail for detail in express_details}

			for detail in express_details:
				if detail.express_id in express_push_id2details:
					express_push_id2details[detail.express_id].append(detail)
				else:
					express_push_id2details[detail.express_id] = [detail]

			for delivery_item in delivery_items:
				push_id = name_number2express_push_id.get(str(delivery_item.express_company_name + '__' + delivery_item.express_number))
				if push_id:
					express_details = express_push_id2details.get(push_id, [])

					for detail in express_details:
						delivery_item.express_details.append({
							'ftime': detail.ftime,
							'context': detail.context
						})




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
			refunding_info = delivery_item_id2refund_info.get(delivery_item.id)
			if refunding_info:
				delivery_item.refunding_info = {
					'cash': refunding_info.cash,
					'weizoom_card_money': refunding_info.weizoom_card_money,
					'integral': refunding_info.integral,
					'integral_money': refunding_info.integral_money,
					'coupon_money': refunding_info.coupon_money,
					'total': refunding_info.total,
					'finished': refunding_info.finished
				}
			else:
				delivery_item.refunding_info = {
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
