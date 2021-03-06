# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from business import model as busniess_model
from business.mall.logistics.limit_zone import ZONE_NAMES, PROVINCE_ID2ZONE


class ProvinceCityRepository(busniess_model.Service):
	def get_zones(self):
		"""
		获取平台的地区信息
		"""
		all_cities = mall_models.City.select()
		all_provinces = mall_models.Province.select()
		all_districts = mall_models.District.select()

		city_id2districts = {}
		for district in all_districts:
			district_info = {
				'district_id': district.id,
				'district_name': district.name
			}
			city_id2districts.setdefault(district.city_id, []).append(district_info)
		province_id2cities = {}
		for city in all_cities:
			city_info = {
				'city_id': city.id,
				'city_name': city.name,
				'districts': city_id2districts[city.id] if city.id in city_id2districts else {}
			}
			province_id2cities.setdefault(city.province_id, []).append(city_info)
		provinces = []
		for province in all_provinces:
			province_info = {
				'province_id': province.id,
				'province_name': province.name,
				'zone_name': PROVINCE_ID2ZONE[province.id],
				'cities': province_id2cities[province.id]
			}

			provinces.append(province_info)

		zones = []
		for zone_name in ZONE_NAMES:
			zones.append({
				'zone_name': zone_name,
				'provinces': filter(lambda province: PROVINCE_ID2ZONE[province['province_id']] == zone_name, provinces)
			})
		return zones