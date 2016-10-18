# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ADeliveryItem(api_resource.ApiResource):
	app = "order"
	resource = "delivery_item"

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
