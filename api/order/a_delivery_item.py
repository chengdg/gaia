# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ADeliveryItem(api_resource.ApiResource):
	app = "order"
	resource = "delivery_item"

	def post(args):

		corp = args['corp']
		delivery_item_bid = args['delivery_item_bid']

		delivery_item = corp.delivery_item_repository.get_delivery_item_by_bid(delivery_item_bid)
		if delivery_item:
			if 'new_ship_info' in args:
				new_ship_info = json.loads(args['new_ship_info'])
				with_logistics = new_ship_info['with_logistics'] == "true"
				with_logistics_trace = new_ship_info['new_ship_info'] == "true"
				company_name_value = new_ship_info['company_name_value']
				leader_name = new_ship_info['leader_name']
				express_number = new_ship_info['express_number']

				is_success, msg = delivery_item.update_ship_info(corp, with_logistics_trace, company_name_value,
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
