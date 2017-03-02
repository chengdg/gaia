# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.order.encode_delivery_item_service import EncodeDeliveryItemService
from business.order.encode_order_service import EncodeOrderService


class ASupplierDeliveryItems(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'order'
	resource = 'supplier_deliver_items'

	@param_required(['corp_id'])
	def get(args):
		filters = json.loads(args.get('filters', '{}'))

		corp = args['corp']
		delivery_item_repository = corp.delivery_item_repository

		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})

		fill_options = {
			'with_products': True,
			# 'with_refunding_info': True,
			'with_express_details': True,
			# 'with_supplier': True,
			# 'with_operation_logs': True
		}


		pageinfo, delivery_items = delivery_item_repository.get_delivery_items(filters, target_page, fill_options)

		encode_delivery_item_service = EncodeDeliveryItemService.get(corp)

		datas = []

		for delivery_item in delivery_items:
			data = {}
			data.update(encode_delivery_item_service.get_base_info(delivery_item))
			# data.update(encode_delivery_item_service.get_refunding_info(delivery_item))
			data.update(encode_delivery_item_service.get_express_details(delivery_item))
			# data.update(encode_delivery_item_service.get_supplier(delivery_item))
			data.update(encode_delivery_item_service.get_products(delivery_item))
			# data.update(encode_delivery_item_service.get_operation_logs(delivery_item))
			datas.append(data)

		# order_dicts = [order.to_dict() for order in orders]
		return {
			'page_info': pageinfo.to_dict(),
			'delivery_items': datas
		}
