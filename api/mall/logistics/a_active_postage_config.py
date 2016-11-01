# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AActivePostageConfig(api_resource.ApiResource):
	"""
	运费模板
	"""
	app = 'mall'
	resource = 'active_postage_config'

	@param_required(['corp_id', 'postage_config_id'])
	def put(args):
		corp = args['corp']
		postage_config_id = args['postage_config_id']
		corp.postage_config_repository.get_postage_config(postage_config_id).set_used(corp)

		return {
			'id': postage_config_id
		}
