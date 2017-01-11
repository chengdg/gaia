# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AProvinceCity(api_resource.ApiResource):
	"""
	获取平台的省市信息
	"""
	app = 'mall'
	resource = 'province_city'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		
		zones = corp.province_city_repository.get_zones()

		return {'zones': zones}
