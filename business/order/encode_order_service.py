# -*- coding: utf-8 -*-
from business import model as business_model
from business.order.encode_delivery_item_service import EncodeDeliveryItemService


class EncodeOrderService(business_model.Service):
	def get_base_info(self, order):
		return {
			'id': order.id,
			'bid': order.bid,
			'pay_interface_type_code': order.pay_interface_type_code,
			'payment_time': order.payment_time,
			'final_price': order.final_price,
			'product_price': order.final_price,
			'edit_money': order.edit_money,
			'bid_with_edit_money': order.bid_with_edit_money,
			'ship_name': order.ship_name,
			'ship_tel': order.ship_tel,
			'ship_area': order.ship_area,
			'ship_area_text': order.ship_area_text,
			'ship_address': order.ship_address,
			'bill_type': order.bill_type,
			'bill': order.bill,
			'postage': order.postage,
			'integral': order.integral,
			'integral_money': order.integral_money,
			'coupon_money': order.coupon_money,
			'coupon_id': order.coupon_id,
			'status_code': order.status_code,
			'customer_message': order.customer_message,
			'supplier_remark': order.customer_message,
			'created_at': order.created_at,

			'webapp_id': order.webapp_id,
			'webapp_user_id': order.webapp_user_id,
			'weizoom_card_money': order.weizoom_card_money,
			'delivery_time': order.delivery_time,
			'is_first_order': order.is_first_order,
			'is_weizoom_order': order.is_weizoom_order,
			'remark': order.remark,
			'pay_money': order.pay_money,
			'promotion_saved_money': order.promotion_saved_money
		}

	def get_extra_promotion_info(self, order):
		return {
			'integral_type': order.integral_type
		}

	def get_extra_coupon_info(self, order):
		return {
			'extra_coupon_info': {
				'bid': order.extra_coupon_info['bid'],
				'type': order.extra_coupon_info['type']
			}

		}

	def get_weizoom_card_info(self, order):
		return {
			'weizoom_card_info': {
				'used_card': order.weizoom_card_info['used_card']
			}
		}

	def get_delivery_items(self, order, delivery_fill_options):
		encode_delivery_item_service = EncodeDeliveryItemService.get(self.corp)

		datas = []
		with_operation_logs = delivery_fill_options.get('with_operation_logs', False)
		for delivery_item in order.delivery_items:
			data = {}
			data.update(encode_delivery_item_service.get_base_info(delivery_item))
			data.update(encode_delivery_item_service.get_refunding_info(delivery_item))
			data.update(encode_delivery_item_service.get_express_details(delivery_item))
			data.update(encode_delivery_item_service.get_supplier(delivery_item))
			data.update(encode_delivery_item_service.get_products(delivery_item))

			if with_operation_logs:
				data.update(encode_delivery_item_service.get_operation_logs(delivery_item))

			datas.append(data)
		return {
			'delivery_items': datas
		}

	def get_operation_logs(self, order):
		return {
			'operation_logs': [{
				                   'action_text': log['action_text'],
				                   'time': log['time'],
				                   'operator': log['operator']
			                   } for log in order.operation_logs]}

	def get_status_logs(self, order):
		return {
			'status_logs':
				[{
					 'from_status_code': log['from_status_code'],
					 'to_status_code': log['to_status_code'],
					 'time': log['time']
				 } for log in order.status_logs]}

	def get_group_buy_info(self, order):
		return {
			'is_group_buy': order.is_group_buy
		}

	def get_refunding_info(self, order):
		return {
			'refunding_info': {
				'cash': order.refunding_info['cash'],
				'weizoom_card_money': order.refunding_info['weizoom_card_money'],
				'integral_money': order.refunding_info['integral_money'],
				'integral': order.refunding_info['integral'],
				'coupon_money': order.refunding_info['coupon_money'],
				'total': order.refunding_info['total'],
			}
		}

	def get_full_money_info(self, order):
		return {
			'origin_weizoom_card_money': order.origin_weizoom_card_money,
			'origin_final_price': order.origin_final_price,
			'save_money': order.save_money
		}

	def get_member_info(self, order):
		return {
			'member_info': {
				'name': order.member_info['name'],
				'id': order.member_info['id'],
				'is_subscribed': order.member_info['is_subscribed'],
			}
		}
