# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.order.delivery_item_ship_service import DeliveryItemShipService


class AShippedDeliveryItems(api_resource.ApiResource):
	app = "order"
	resource = "shipped_delivery_items"

	@param_required(['ship_infos'])
	def put(args):
		"""
		批量创建已发货订单

		发货基本信息：
		- delivery_item_bid
		- with_logistics
		- with_logistics_trace
		- express_company_name: 为中文名称，如申通快递
		- express_number
		- leader_name
		@return:
		"""

		infos = json.loads(args["ship_infos"])
		corp = args['corp']

		ship_infos = [
			{
				'delivery_item_bid': x['delivery_item_bid'],
				'with_logistics': x['with_logistics'] in ('true', True),
				'with_logistics_trace': x['with_logistics_trace'] in ('true', True),
				'company_name_value': x['express_company_name_value'],
				'express_number': x['express_number'],
				'leader_name': x['leader_name'],
			} for x in infos]

		delivery_item_ship_service = DeliveryItemShipService.get(corp)

		_tmp_ship_infos = delivery_item_ship_service.ship_delivery_items(ship_infos)

		ship_result = [{
			               "delivery_item_bid": info["delivery_item_bid"],
			               "is_success": info['is_success'],
			               "error_info": info['error_info']

		               } for info in _tmp_ship_infos]
		return ship_result
