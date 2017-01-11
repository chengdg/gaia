# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.shipper import Shipper


class AShippers(api_resource.ApiResource):
	app = 'mall'
	resource = 'a_shippers'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		shippers = corp.shipper_repository.get_shippers()

		return { 'shippers': shippers }