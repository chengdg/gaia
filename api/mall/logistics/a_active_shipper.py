# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AActiveShipper(api_resource.ApiResource):
	"""
	启用发货人
	"""
	app = 'mall'
	resource = 'active_shipper'

	@param_required(['corp_id', 'id'])
	def put(args):
		corp = args['corp']

		id = args['id']
		corp.shipper_repository.get_shipper(id).set_used()

		return {
			'id': id
		}
