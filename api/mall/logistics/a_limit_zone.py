# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.logistics.limit_zone import LimitZone
from business.mall.corporation_factory import CorporationFactory


class ALimitZone(api_resource.ApiResource):
	"""
	单个限定区域
	"""
	app = 'mall'
	resource = 'limit_zone'

	@param_required(['corp_id', 'id'])
	def get(args):
		corp = args['corp']
		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		CorporationFactory.set(weizoom_corp)
		limit_zone = weizoom_corp.limit_zone_repository.get_limit_zone_by_id(args['id'])
		CorporationFactory.set(corp)
		data = {
			'id': limit_zone.id,
			'name': limit_zone.name,
			'zones': limit_zone.zones
		}
		return data

	@param_required(['corp_id', 'name', 'limit_provinces', 'limit_cities'])
	def put(args):
		corp = args['corp']
		name = args['name']
		limit_provinces = json.loads(args.get('limit_provinces', '[]'))
		limit_cities = json.loads(args.get('limit_cities', '[]'))
		LimitZone.create(
			{'corp_id': corp.id, 'name': name, 'limit_provinces': limit_provinces, 'limit_cities': limit_cities})
		return {}

	@param_required(['corp_id', 'id', 'name', 'limit_provinces', 'limit_cities'])
	def post(args):
		corp = args['corp']
		id = args['id']
		name = args['name']
		limit_provinces = json.loads(args.get('limit_provinces', '[]'))
		limit_cities = json.loads(args.get('limit_cities', '[]'))
		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		CorporationFactory.set(weizoom_corp)
		limit_zone = weizoom_corp.limit_zone_repository.get_limit_zone_by_id(id)
		CorporationFactory.set(corp)
		limit_zone.update(name, limit_provinces, limit_cities)
		return {}

	@param_required(['corp', 'id'])
	def delete(args):
		corp = args['corp']
		corp.limit_zone_repository.delete_limit_zone(args['id'])
		return {}
