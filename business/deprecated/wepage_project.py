# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from business import model as busness_model
from db.mall import models as mall_models


class WepageProject(busness_model.Model):
	"""
	微页面项目
	"""
	__slots__ = (
		'id',
		'workspace_id',
		'name',
		'inner_name',
		'type',
		'css',
		'pagestore',
		'datasource_project_id',
		'template_project_id',
		'is_enable',
		'cover_name',
		'site_title',
		'is_active'
	)

	def __init__(self, model):
		busness_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)