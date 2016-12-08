# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.order.encode_order_service import EncodeOrderService


class AMemberOrderStatistics(api_resource.ApiResource):
	"""
	会员订单统计数据
	"""
	app = 'order'
	resource = 'orders'

	@param_required(['corp'])
	def get(args):
		pass