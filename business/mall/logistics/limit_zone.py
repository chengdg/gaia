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
		'zones'
	)

	def __init__(self, model):
		busness_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.zones = self.__get_zones()

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

	def update(self, name='', limit_provinces=[], limit_cities=[]):
		"""
		更新限定区域
		"""
		mall_models.ProductLimitZoneTemplate.update(
			name=name,
			provinces=','.join(limit_provinces),
			cities=','.join(limit_cities)
		).dj_where(id=self.id).execute()

	def __get_zones(self):
		if not self.context['db_model'].provinces:
			return []
		province_ids = self.context['db_model'].provinces.split(',')
		city_ids = self.context['db_model'].cities.split(',') if self.context['db_model'].cities else []
		limit_zone_provinces = mall_models.Province.select().dj_where(id__in=province_ids)
		limit_zone_cities = mall_models.City.select().dj_where(id__in=city_ids)
		provinces = []
		zone_names = []
		for province in limit_zone_provinces:
			province_info = {
				'province_id': province.id,
				'province_name': province.name,
				'zone_name': PROVINCE_ID2ZONE[province.id],
				'cities': []
			}
			for city in filter(lambda city: city.province_id == province.id, limit_zone_cities):
				province_info['cities'].append({
					'city_id': city.id,
					'city_name': city.name
				})
			provinces.append(province_info)
			if province_info['zone_name'] not in zone_names:
				zone_names.append(province_info['zone_name'])
		zones = []
		for zone_name in zone_names:
			zones.append({
				'zone_name': zone_name,
				'provinces': filter(lambda province: province['zone_name'] == zone_name,
									provinces)
			})
		return zones