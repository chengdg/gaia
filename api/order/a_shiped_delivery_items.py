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
		- delivery_item_id
		- delivery_item_bid
		- express_company_name
		- express_number
		- leader_name
		- is_100
		@return:
		"""

		infos = json.loads(args)

		corp = args['corp']

		ship_infos = [
			{
				'delivery_item_bid': x['delivery_item_bid'],
				'express_company_name': x['express_company_name'],
				'express_number': x['express_number'],
				'leader_name': x['leader_name'],
				'is_100': x['delivery_item_id'] == "true"

			} for x in infos]

		delivery_item_ship_service = DeliveryItemShipService.get(corp)

		success_data, error_data = delivery_item_ship_service.ship_delivery_items(ship_infos)

		return {
			'success_data': success_data,
			'error_data': error_data
		}
