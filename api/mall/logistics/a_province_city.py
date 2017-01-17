# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.logistics.limit_zone import ZONE_NAMES, PROVINCE_ID2ZONE

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

		datas=[]
		provinces = []
		for zone in zones:
			for _province in zone['provinces']:
				cities = []
				_cities = _province['cities']
				for _city in _cities:
					districts = []
					_districts = _city['districts']
					for _district in _districts:
						districts.append({
							'district_id': _district['district_id'],
							'district_name': _district['district_name']
						})
					cities.append({
						'city_id': _city['city_id'],
						'city_name': _city['city_name'],
						'districts': districts
					})
				provinces.append({
					'province_id': _province['province_id'],
					'province_name': _province['province_name'],
					'zone_name': _province['zone_name'],
					'cities': cities
				})

		datas=[]
		for zone_name in ZONE_NAMES:
			datas.append({
				'zone_name': zone_name,
				'provinces': filter(lambda province: PROVINCE_ID2ZONE[province['province_id']] == zone_name, provinces)
			})

		return {'zones': datas}
