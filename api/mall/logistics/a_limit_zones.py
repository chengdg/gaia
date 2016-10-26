# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ALimitZones(api_resource.ApiResource):
	"""
	限定区域集合
	"""
	app = 'mall'
	resource = 'limit_zones'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		limit_zones = corp.limit_zone_repository.get_limit_zones()
		datas = []
		for limit_zone in limit_zones:
			data = {
				'id': limit_zone.id,
				'name': limit_zone.name,
				'zones': limit_zone.zones
			}
			datas.append(data)
		return {"limit_zones": datas}


