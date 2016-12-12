# -*- coding: utf-8 -*-
"""
出货单发货服务
"""

from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from business import model as business_model
from db.mall import models as mall_models


class DeliveryItemShipService(business_model.Service):
	def ship_delivery_items(self, ship_infos):
		for ship_info in ship_infos:
			delivery_item_bid = ship_info['delivery_item_bid']
			company_name_value = ''
			express_number = ''
			leader_name = ship_info['leader_name']

			# 校验订单存在
			if "-" in delivery_item_bid:  # 过滤掉改价生产的字符串
				delivery_item_bid = delivery_item_bid.split('-')[0]

			delivery_item = self.corp.delivery_item_repository.get_delivery_item_by_bid(delivery_item_bid)
			if not delivery_item:
				ship_info["error_info"] = u"订单号错误"
				ship_info["is_success"] = False
				continue

			# 校验订单状态
			if delivery_item.status != mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
				ship_info["error_info"] = u"订单状态错误"
				ship_info["is_success"] = False
				continue

			# 如果使用物流
			with_logistics = ship_info['with_logistics']
			if with_logistics:
				company_name_value = ship_info['company_name_value']
				leader_name = ship_info['leader_name']
				express_number = ship_info['express_number']

				# 校验快递单号非空
				if not express_number:
					ship_info["error_info"] = u"格式错误"
					ship_info["is_success"] = False
					continue

				# 如果使用快递追踪
				with_logistics_trace = ship_info['with_logistics_trace']
				if with_logistics_trace:
					# 校验快递公司名称
					all_companies = self.corp.express_delivery_repository.get_companies()  # 获得系统支持的所有快递公司
					selected_company = None
					for company in all_companies:  # 检查用户提交的是否是合法快递公司
						if company.value == company_name_value:
							selected_company = company
							break
					if not selected_company:
						ship_info["error_info"] = u"快递名称错误"
						ship_info["is_success"] = False
						continue
				else:
					company_name_value = ship_info['company_name_value']

			else:
				with_logistics_trace = False  # 防止发来不用物流却又要求物流追踪的
			try:
				is_success, msg = delivery_item.ship(self.corp, with_logistics_trace,
				                                     company_name_value, express_number, leader_name)

				if is_success:
					ship_info['error_info'] = u""
					ship_info["is_success"] = True
				else:
					ship_info['error_info'] = u"发送异常"
					ship_info["is_success"] = False
			except:
				ship_info["error_info"] = u"发送异常"
				ship_info['is_success'] = False
				watchdog.alert({
					"uuid": "ship_error",
					"hint": u"发送出货单异常",
					"ship_info": ship_info,
					'traceback': unicode_full_stack()
				})

		return ship_infos
