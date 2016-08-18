# -*- coding: utf-8 -*-
"""@package wapi.mall.a_data
服务演示数据

"""
#import copy
#from datetime import datetime
#import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.demo.data import Data
from api.decorators import access_token_required
import logging

class AData(api_resource.ApiResource):
	"""
	优惠券
	"""
	app = 'demo'
	resource = 'data'

	@param_required(['id'])
	@access_token_required()
	def get(args):
		logging.info('args: {}'.format(args))
		data = Data.get({
			"id": args.get('id', None)
		})

		return {
			"id": data.id,
			"name": data.name,
			"age": data.age,
			"args": args
		}
