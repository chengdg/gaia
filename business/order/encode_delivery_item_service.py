# -*- coding: utf-8 -*-
from business import model as business_model


class EncodeDeliveryItemService(business_model.Service):
	def get_base_info(self, delivery_item):
		return {
			'id': delivery_item.id,
			'bid': delivery_item.bid,
			'origin_order_id': delivery_item.origin_order_id,
			'webapp_id': delivery_item.webapp_id,
			'webapp_user_id': delivery_item.webapp_user_id,
			'postage': delivery_item.postage,
			'status_code': delivery_item.status_code,
			'payment_time': delivery_item.payment_time,
			'area': delivery_item.area,
			'ship_name': delivery_item.ship_name,
			'express_company_name_value': delivery_item.express_company_name_value,
			'express_company_name_text': delivery_item.express_company_name_text,
			'express_number': delivery_item.express_number,
			'leader_name': delivery_item.leader_name,
			'created_at': delivery_item.created_at,
			'with_logistics_trace': delivery_item.with_logistics_trace,
			'with_logistics': delivery_item.with_logistics,
			'customer_message': delivery_item.customer_message
		}

	def get_express_details(self, delivery_item):
		return {
			'express_details': [
				{
					'ftime': detail['ftime'],
					'context': detail['context'],
				} for detail in delivery_item.express_details
				]}

	def get_products(self, delivery_item):
		return {'products': [{
			                     'id': product.id,
			                     'name': product.name,
			                     'origin_price': product.origin_price,
			                     'sale_price': product.sale_price,
			                     'show_sale_price': product.show_sale_price,
			                     'count': product.count,
			                     'thumbnails_url': product.thumbnails_url,
			                     'is_deleted': product.is_deleted,
			                     'weight': product.weight,
			                     'total_origin_price': product.total_origin_price,
			                     'product_model_name_texts': product.product_model_name_texts,
			                     'promotion_info': {
				                     'type': product.promotion_info['type'],
				                     'integral_money': product.promotion_info['integral_money'],
				                     'integral_count': product.promotion_info['integral_count'],
				                     'grade_discount_money': product.promotion_info['grade_discount_money'],
				                     'promotion_saved_money': product.promotion_info['promotion_saved_money'],
			                     }
		                     } for product in delivery_item.products]}

	def get_operation_logs(self, delivery_item):
		return {
			'operation_logs': [{
				                   'action_text': log['action_text'],
				                   'time': log['time'],
				                   'operator': log['operator']
			                   } for log in delivery_item.operation_logs]}

	def get_refunding_info(self, delivery_item):
		return {
			'refunding_info': {
				"cash": delivery_item.refunding_info['cash'],
				"weizoom_card_money": delivery_item.refunding_info['weizoom_card_money'],
				"member_card_money": delivery_item.refunding_info['member_card_money'],
				"integral": delivery_item.refunding_info['integral'],
				"integral_money": delivery_item.refunding_info['integral_money'],
				"coupon_money": delivery_item.refunding_info['coupon_money'],
				"total": delivery_item.refunding_info['total'],
				"finished": delivery_item.refunding_info['finished'],
				"total_can_refund": delivery_item.refunding_info['total_can_refund']
			}
		}

	def get_supplier(self, delivery_item):
		return {
			'supplier_info': {
				'name': delivery_item.supplier_info['name'],
				'supplier_type': delivery_item.supplier_info['supplier_type']
			}
		}
