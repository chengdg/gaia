# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from business import model as busness_model
from db.mall import models as mall_models

ZONE_NAMES = [u'直辖市', u'华北-东北', u'华东地区', u'华南-华中', u'西北-西南', u'其它']

PROVINCE_ID2ZONE = {
    1: u'直辖市',
    2: u'直辖市',
    3: u'华北-东北',
    4: u'华北-东北',
    5: u'华北-东北',
    6: u'华北-东北',
    7: u'华北-东北',
    8: u'华北-东北',
    9: u'直辖市',
    10: u'华东地区',
    11: u'华东地区',
    12: u'华东地区',
    13: u'华东地区',
    14: u'华东地区',
    15: u'华东地区',
    16: u'华南-华中',
    17: u'华南-华中',
    18: u'华南-华中',
    19: u'华南-华中',
    20: u'华南-华中',
    21: u'华南-华中',
    22: u'直辖市',
    23: u'西北-西南',
    24: u'西北-西南',
    25: u'西北-西南',
    26: u'西北-西南',
    27: u'西北-西南',
    28: u'西北-西南',
    29: u'西北-西南',
    30: u'西北-西南',
    31: u'西北-西南',
    32: u'其它',
    33: u'其它',
    34: u'其它',
}

class LimitZone(busness_model.Model):
	"""
	限定区域
	"""
	__slots__ = (
		'id',
		'name',
		'provinces',
		'cities'
	)

	def __init__(self, model):
		busness_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)
			self.provinces = self.provinces.split(',')
			self.cities = self.cities.split(',') if self.cities else []

	@staticmethod
	@param_required(['corp_id', 'name', 'limit_provinces', 'limit_cities'])
	def create(args):
		limit_zone = mall_models.ProductLimitZoneTemplate.create(
			owner=args['corp_id'],
			name=args['name'],
			provinces=','.join(args['limit_provinces']),
			cities=','.join(args['limit_cities'])
		)
		return limit_zone

	@staticmethod
	@param_required(['corp_id', 'id', 'name', 'limit_provinces', 'limit_cities'])
	def update(args):
		mall_models.ProductLimitZoneTemplate.update(
			name=args['name'],
			provinces=','.join(args['limit_provinces']),
			cities=','.join(args['limit_cities'])
		).dj_where(owner_id=args['corp_id'], id=args['id']).execute()

	def fill_limit_zone_detail(self):
		limit_zone_provinces = mall_models.Province.select().dj_where(id__in=self.provinces)
		limit_zone_cities = mall_models.City.select().dj_where(id__in=self.cities)
		provinces = []
		zone_names = []
		for province in limit_zone_provinces:
			province_info = {
				'province_id': province.id,
				'province_name': province.name,
				'zone_name': PROVINCE_ID2ZONE[province.id],
				'cities': []
			}
			province_info = self.__rename_province(province_info)
			for city in filter(lambda city: city.province_id == province.id, limit_zone_cities):
				province_info['cities'].append({
					'city_id': city.id,
					'city_name': city.name
				})
			provinces.append(province_info)
			print province_info
			if province_info['zone_name'] not in zone_names:
				zone_names.append(province_info['zone_name'])
		limit_zone_detail = []
		for zone_name in zone_names:
			limit_zone_detail.append({
				'zone_name': zone_name,
				'provinces': filter(lambda province: province['zone_name'] == zone_name,
									provinces)
			})
		return limit_zone_detail

	def __rename_province(self, province):
		if province['province_id'] == 5:
			province['province_name'] = u'内蒙古'
		elif province['province_id'] == 20:
			province['province_name'] = u'广西'
		elif province['province_id'] == 26:
			province['province_name'] = u'西藏'
		elif province['province_id'] == 30:
			province['province_name'] = u'宁夏'
		elif province['province_id'] == 31:
			province['province_name'] = u'新疆'
		elif province['province_id'] == 32:
			province['province_name'] = u'香港'
		elif province['province_id'] == 33:
			province['province_name'] = u'澳门'
		elif province['province_id'] == 34:
			province['province_name'] = u'台湾'
		return province