# -*- coding: utf-8 -*-
"""
出货单发货服务
"""

from bdem import msgutil
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.supplier import Supplier
from business.order.delivery_item_product_repository import DeliveryItemProductRepository
from db.express import models as express_models
from db.mall import models as mall_models


class DeliveryItemShipService(business_model.Service):
	def ship_delivery_items(self, ship_infos):
		error_data = []
		success_data = []
		for ship_info in ship_infos:
			is_100 = ship_info['is_100']

			if is_100:
				# 校验快递公司名称 todo
				pass
			# ship_info["error_info"] = u"快递名称错误"
			# error_data.append(ship_info)

			delivery_item_bid = ship_info['delivery_item_bid']
			if "-" in delivery_item_bid:
				delivery_item_bid = delivery_item_bid.split('-')[0]

			delivery_item = self.corp.delivery_item_repository.get_delivery_item(delivery_item_bid)

			if not delivery_item:
				ship_info["error_info"] = u"订单号错误"
				error_data.append(ship_info)
				continue
			elif not ship_info['express_number']:
				ship_info["error_info"] = u"格式错误"
				error_data.append(ship_info)
				continue
			elif delivery_item.status != mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
				ship_info["error_info"] = u"订单状态错误"
				error_data.append(ship_info)
				continue
			else:
				try:
					delivery_item.ship(self.corp)
					is_success, msg = success_data.append(ship_info)
					if is_success:
						success_data.append(ship_info)
					else:
						ship_info['error_info'] = u"发送异常"
						error_data.append(ship_info)
				except:
					ship_info["error_info"] = u"发送异常"
					watchdog.alert({
						"uuid": "ship_error",
						"hint": u"发送出货单异常",
						"ship_info": ship_info
					})
					error_data.append(ship_info)

		return success_data, error_data
