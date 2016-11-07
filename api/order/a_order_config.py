# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class AOrderConfig(api_resource.ApiResource):
	"""
	订单设置
	"""
	app = 'order'
	resource = 'config'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		order_config = corp.order_config_repository.get_order_config()

		data = {
			"order_expired_day": order_config.order_expired_day,
			"is_share_page": order_config.is_share_page,
			"background_image": order_config.background_image,
			"share_image": order_config.share_image,
			"share_describe": order_config.share_describe,
			"material_id": order_config.material_id,
			"title": order_config.title
		}

		return data

	@param_required([
		'corp_id',
		'order_expired_day:int',
		'is_share_page:bool',
		'?background_image:str',
		'?share_image:str',
		'?share_describe:str',
		'?material_id:int'
	])
	def post(args):
		corp = args['corp']

		order_config = corp.order_config_repository.get_order_config(args['is_share_page'])
		order_config.update(args)

		data = {
			"order_expired_day": order_config.order_expired_day,
			"is_share_page": order_config.is_share_page,
			"background_image": order_config.background_image,
			"share_image": order_config.share_image,
			"share_describe": order_config.share_describe,
			"material_id": order_config.material_id,
			"title": order_config.title
		}

		return data