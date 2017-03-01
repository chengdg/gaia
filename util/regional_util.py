# -*- coding: utf-8 -*-

from db.mall import models as mall_models

ID2PROVINCE = dict([(p.id, p.name) for p in mall_models.Province.select()])
ID2CITY = dict([(c.id, c.name) for c in mall_models.City.select()])
ID2DISTRICT = dict([(d.id, d.name) for d in mall_models.District.select()])


def get_str_value_by_string_ids(str_ids):
	try:
		if str_ids != '' and str_ids:
			# cache = get_cache('mem')
			# ship_address = cache.get(str_ids)
			# TODO: 重新加入缓存
			ship_address = ''

			area_args = str_ids.split('_')
			ship_address = ''
			current_area = ''
			for index, area in enumerate(area_args):

				if index == 0:
					# current_area = mall_models.Province.get(id=int(area))
					current_area = ID2PROVINCE.get(int(area), None)
				elif index == 1:
					# current_area = mall_models.City.get(id=int(area))
					current_area = ID2CITY.get(int(area), None)

				elif index == 2:
					current_area = ID2DISTRICT.get(int(area), None)

				if current_area:
					ship_address = ship_address + ' ' + current_area

			return u'{}'.format(ship_address.strip())
		else:
			return None
	except:
		return ''
