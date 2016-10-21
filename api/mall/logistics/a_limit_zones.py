# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ALimitZones(api_resource.ApiResource):
	"""
	限定区域集合
	"""
	app = 'mall'
	resource = 'limit_zones'

	@param_required(['corp'])
	def get(args):
		corp = args['corp']
		limit_zones = corp.limit_zone_repository.get_limit_zones()
		datas = []
		for limit_zone in limit_zones:
			datas.append(
				{
					'id': limit_zone.id,
					'name': limit_zone.name,
					'limit_provinces': limit_zone.provinces.split(','),
					'limit_cities': limit_zone.cities.split(',')
				}
			)
		return datas


