# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from eaglet.core import paginator

from business import model as business_model


provinces = list(mall_models.Province.select())
cities = list(mall_models.City.select())
districts = list(mall_models.District.select())

ID2PROVINCE = dict([(p.id, p.name) for p in provinces])
ID2CITY = dict([(c.id, c.name) for c in cities])
ID2DISTRICT = dict([(d.id, d.name) for d in districts])

PROVINCE2ID = dict([(p.name, p.id) for p in provinces])
CITY2ID = dict([(c.name, c.id) for c in cities])
DISTRICT2ID = dict([(d.name, d.id) for d in districts])


class EncodeDistrictService(business_model.Service):
	"""
	对行政区进行编码解码的Service
	"""
	def decode(self, area_codes):
		"""
		将"1_1_1"这样的编码解码为"北京市 北京市 东城区"
		"""
		area_codes = area_codes.strip()
		if not area_codes:
			return None

		items = []
		area_codes = area_codes.split('_')
		for index, area_code in enumerate(area_codes):
			area_code = int(area_code)
			if index == 0:
				curren_area = ID2PROVINCE[area_code]
			elif index == 1:
				curren_area = ID2CITY[area_code]
			elif index == 2:
				curren_area = ID2DISTRICT[area_code]
			items.append(curren_area)

		return ' '.join(items)

	def encode(slef, area_values):
		"""
		将"北京市 北京市 东城区"这样的编码解码为"1_1_1"
		"""
		area_values = area_values.strip()
		if not area_values:
			return None

		items = []
		area_values = area_values.split(' ')
		for index, area_value in enumerate(area_values):
			if index == 0:
				area_code = PROVINCE2ID[area_value]
			elif index == 1:
				area_code = CITY2ID[area_value]
			elif index == 2:
				area_code = DISTRICT2ID[area_value]
			items.append(str(area_code))

		return '_'.join(items)

