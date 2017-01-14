# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.shipper import Shipper


class AShippers(api_resource.ApiResource):
	app = 'mall'
	resource = 'shippers'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		shippers = corp.shipper_repository.get_shippers()

		datas = []
		for shipper in shippers:
			data = {
				'id': shipper.id,
				'name': shipper.name,
				'tel_number': shipper.tel_number,
				'province': shipper.province,
				'city': shipper.city,
				'district': shipper.district,
				'address': shipper.address,
				'company_name': shipper.company_name,
				'postcode': shipper.postcode,
				'remark': shipper.remark,
				'is_active': shipper.is_active
			}
			datas.append(data)

		return { 'shippers': datas }