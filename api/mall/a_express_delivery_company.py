# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.tools.express import util as tools_express_util

from business.mall.express_delivery import ExpressDelivery


class AExpressDeliveryCompany(api_resource.ApiResource):
	"""
	积分规则设置
	"""
	app = 'mall'
	resource = 'express_delivery_company'

	@param_required(['owner_id'])
	def get(args):
		'''
		@params source 如果有 init_express_deliverys 取所有物流，
			如果没有，取已经添加的物流
		'''
		source = args.get('source', '')
		data = tools_express_util.get_express_company_json()
		express_deliverys = ExpressDelivery.from_owner_id({'owner_id': args['owner_id']})
		# 配置管理-
		if source == 'init_express_deliverys':
			# 过滤已有的快递公司
			result_express_deliverys = []
			if len(express_deliverys) == 0:
				result_express_deliverys = data
			else:
				express_values = [e['express_value'] for e in express_deliverys]
				for item in data:
					if item['value'] in express_values:
						continue
					result_express_deliverys.append(item)

		# 订单管理发货时获得物流公司信息
		else:

			if len(express_deliverys) > 0:
				# 获取 物流名称管理  中的物流信息
				result_express_deliverys = []
				for express_delivery in express_deliverys:
					result_express_deliverys.append({
						"name": express_delivery['name'],
						"expressNumber": express_delivery['express_number'],
						"expressValue": express_delivery['express_value'],
					})
			else:
				# 获取 全部的物流信息
				result_express_deliverys = data

		return {
			'express_delivery_companies': result_express_deliverys
		}