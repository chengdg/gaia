# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AIntegralStrategy(api_resource.ApiResource):
	"""
	积分规则设置
	"""
	app = 'mall'
	resource = 'integral_strategy'

	@param_required(['owner_id'])
	def get(args):
		return {}

	@param_required(['owner_id'])
	def post(args):
		pass