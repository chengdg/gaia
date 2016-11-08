# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required


class AWepageWorkspaceProject(api_resource.ApiResource):
	"""
	获取project
	"""
	app = 'deprecated'
	resource = 'wepage_workspace_project'

	@param_required(['corp_id', 'project_id'])
	def get(args):
		corp = args['corp']
		project_id = int(args['project_id'])
		project = corp.wepage_project.get_wepage_project(project_id)
		return {'workspace_id': project.workspace_id, 'id': project.id, 'is_active': project.is_active}

