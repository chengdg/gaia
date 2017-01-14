# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.shipper import Shipper


class AShipper(api_resource.ApiResource):
	app = 'mall'
	resource = 'shipper'

	@param_required(['corp_id', 'id'])
	def get(args):
		corp = args['corp']

		shipper = corp.shipper_repository.get_shipper(args['id'])

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

		return { 'shipper': data }

	@param_required(['corp_id', 'id','name','tel_number','province','city','district','address','postcode','company_name','remark','is_active:bool'])
	def post(args):
		corp = args['corp']

		is_active = args.get('is_active', False)

		shipper = corp.shipper_repository.get_shipper(args['id'])
		shipper.update(args['name'],args['tel_number'],args['province'],args['city'],args['district'],args['address'],args['postcode'],args['company_name'],args['remark'],is_active,
		)
		return {}

	@param_required(['corp_id','name','tel_number','province','city','district','address','postcode','company_name','remark','is_active:bool'])
	def put(args):
		'''
		创建发货人
		'''
		is_active = args.get('is_active', False)
		shipper = Shipper.create({
			'name' : args['name'],
			'tel_number' : args['tel_number'],
			'province' : args['province'],
			'city' : args['city'],
			'district' : args['district'],
			'address' : args['address'],
			'postcode' : args['postcode'],
			'company_name' : args['company_name'],
			'remark' : args['remark'],
			'is_active' : is_active,
		})
		return {}

	@param_required(['corp', 'id'])
	def delete(args):
		corp = args['corp']
		shipper = corp.shipper_repository.delete_shipper(args['id'])

