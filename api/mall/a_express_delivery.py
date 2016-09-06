# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.express_delivery import ExpressDelivery


class AExpressDelivery(api_resource.ApiResource):
	app = 'mall'
	resource = 'express_delivery'

	@param_required(['owner_id', 'name', 'express_number', 'express_value'])
	def put(args):
		'''
		创建物流公司
		'''
		express_delivery = ExpressDelivery.create({
			'owner_id': args['owner_id'],
			'name': args['name'],
			'express_number': args['express_number'],
			'express_value': args['express_number'],
			'remark': args.get('remark', '')
		})
		return {
			'express_delivery': express_delivery.to_dict()
		}

	@param_required(['owner_id', 'id'])
	def post(args):
		'''
		@params id 是源id src_id
		@params dst_id
		'''
		express_delivery = ExpressDelivery.from_id({'owner_id': args['owner_id'], 'id': args['id']})
		if express_delivery:
			if 'dst_id' in args:
				express_delivery.update_display_index(args['owner_id'], args['dst_id'], args['id'])
			else:
				express_delivery.update(args.get('name'),args.get('express_number'), args.get('express_value'), args.get('remark', ''))
			return {}
		else:
			msg = u'id {} not exist'.format(args['id'])
			return 500, {'msg': msg}
	@param_required(['owner_id', 'id'])
	def get(args):
		express_delivery = ExpressDelivery.from_id({'owner_id': args['owner_id'], 'id': args['id']})
		if express_delivery:
			# import pdb
			# pdb.set_trace()
			return {
				'express_delivery': express_delivery.to_dict()
			}
		else:
			msg = u'id {} not exist'.format(args['id'])
			return 500, {'msg': msg}

	@param_required(['owner_id', 'id'])
	def delete(args):
		express_delivery = ExpressDelivery.from_id({'owner_id': args['owner_id'], 'id': args['id']})
		if express_delivery:
			express_delivery.delete()
			return {}
		else:
			msg = u'id {} not exist'.format(args['id'])
			return 500, {'msg': msg}

