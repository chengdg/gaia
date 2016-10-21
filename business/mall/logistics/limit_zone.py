# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from business import model as busness_model
from db.mall import models as mall_models

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
			self.__init_slot_from_model(model)

	@staticmethod
	@param_required(['corp_id', 'name', 'limit_provinces', 'limit_cities'])
	def create(args):
		limit_zone = mall_models.ProductLimitZoneTemplate.create(
			owner_id=args['corp_id'],
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
