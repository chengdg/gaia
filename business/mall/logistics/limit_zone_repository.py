# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.mall import models as mall_models
from business import model as busniess_model
from business.mall.logistics.limit_zone import LimitZone


class LimitZoneRepository(busniess_model.Service):
	def get_limit_zones(self):
		"""
		获取corp中所有的限定区域
		"""
		limit_zone_models = mall_models.ProductLimitZoneTemplate.select().dj_where(owner_id=self.corp.id)
		datas = []
		for model in limit_zone_models:
			limit_zone = LimitZone(model)
			data = {
				"id": limit_zone.id,
				"name": limit_zone.name,
				"limit_zone": limit_zone.fill_limit_zone_detail()
			}
			datas.append(data)
		return datas

	def get_limit_zone(self, limit_zone_id):
		"""
		获取指定的limit zone
		"""
		limit_zone_model = mall_models.ProductLimitZoneTemplate.select().dj_where(owner_id=self.corp.id, id=limit_zone_id).get()

		limit_zone = LimitZone(limit_zone_model)
		data = {
			"id": limit_zone.id,
			"name": limit_zone.name,
			"limit_zone": limit_zone.fill_limit_zone_detail()
		}
		return data

	def delete_limit_zone(self, limit_zone_id):
		"""
		删除指定的limit zone
		"""
		mall_models.ProductLimitZoneTemplate.delete().dj_where(owner_id=self.corp.id, id=limit_zone_id).execute()