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
		return {"limit_zones": limit_zones}


