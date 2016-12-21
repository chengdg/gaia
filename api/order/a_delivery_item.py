# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.encode_delivery_item_service import EncodeDeliveryItemService

class ADeliveryItem(api_resource.ApiResource):
	app = "order"
	resource = "delivery_item"

	@param_required(['delivery_item_id'])
	def get(args):
		"""
		相对于订单列表的增量信息：状态日志、操作日志、物流信息、完整的促销信息、优惠券信息
		@return:
		"""

		# todo 操作日志
		delivery_item_id = args['delivery_item_id']

		corp = args['corp']
		delivery_item_repository = corp.delivery_item_repository

		delivery_fill_options = {
			'with_products': True,
			'with_refunding_info': True,
			'with_express_details': True,
			'with_supplier': True,
			'with_operation_logs': True
		}

		delivery_item = delivery_item_repository.get_delivery_item(delivery_item_id, delivery_fill_options)

		encode_delivery_item_service = EncodeDeliveryItemService.get(corp)
		data = {}
		data.update(encode_delivery_item_service.get_base_info(delivery_item))
		data.update(encode_delivery_item_service.get_refunding_info(delivery_item))
		data.update(encode_delivery_item_service.get_express_details(delivery_item))
		data.update(encode_delivery_item_service.get_supplier(delivery_item))
		data.update(encode_delivery_item_service.get_products(delivery_item))
		data.update(encode_delivery_item_service.get_operation_logs(delivery_item))

		if delivery_item:
			return {'delivery_item': data}
		else:
			return 500, {}

	@param_required(['corp'])
	def post(args):

		corp = args['corp']
		delivery_item_id = args['delivery_item_id']

		delivery_item = corp.delivery_item_repository.get_delivery_item(delivery_item_id)
		if delivery_item:
			if 'new_ship_info' in args:
				new_ship_info = json.loads(args['new_ship_info'])

				with_logistics = new_ship_info['with_logistics'] == "true"
				with_logistics_trace = new_ship_info['with_logistics_trace'] == "true"
				express_company_name_value = new_ship_info['express_company_name_value']
				leader_name = new_ship_info['leader_name']
				express_number = new_ship_info['express_number']

				is_success, msg = delivery_item.update_ship_info(corp, with_logistics_trace, express_company_name_value,
				                                                 express_number, leader_name)

			else:
				is_success = False
				msg = 'error args'

			if is_success:
				return {}
			else:
				return 500, {'msg': msg}
		else:
			return 500, {}
