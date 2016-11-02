# -*- coding: utf-8 -*-

from db.mall import models as mall_models
from business import model as busniess_model
from business.deprecated.wepage_project import WepageProject


class WepageProjectRepository(busniess_model.Service):
	def get_wepage_project(self, project_id):
		"""
		获取微页面的项目
		"""
		if project_id == 0:
			project_model = mall_models.Project.select().dj_where(owner_id=self.corp.id, is_active=True).first()
		else:
			project_model = mall_models.Project.select().dj_where(id=project_id).get()
		return WepageProject(project_model)