# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.postage_config import PostageConfig
from business.mall.postage_config_factory import PostageConfigFactory


class APostageConfig(api_resource.ApiResource):
	"""
	运费模板
	"""
	app = 'mall'
	resource = 'postage_config'

	@param_required(['corp_id', 'id'])
	def get(args):
		corp = args['corp']
		postage_config = corp.postage_config_repository.get_postage_config(args['id'])

		default_config = postage_config.default_config
		data = {
			"id": postage_config.id,
			"name": postage_config.name,
			"is_used": postage_config.is_used,
			"is_system_level_config": postage_config.is_system_level_config,
			"is_enable_special_config": postage_config.is_enable_special_config,
			"is_enable_free_config": postage_config.is_enable_free_config,
			"default_config": {
				"first_weight": default_config.first_weight,
				"first_weight_price": default_config.first_weight_price,
				"added_weight": default_config.added_weight,
				"added_weight_price": default_config.added_weight_price
			},
			'special_configs': [],
			'free_configs': []
		}

		for special_config in postage_config.special_configs:
			data['special_configs'].append({
				"id": special_config.id,
				"destinations": special_config.destinations,
				"first_weight": special_config.first_weight,
				"first_weight_price": special_config.first_weight_price,
				"added_weight": special_config.added_weight,
				"added_weight_price": special_config.added_weight_price
			})

		for free_config in postage_config.free_configs:
			data['free_configs'].append({
				"id": free_config.id,
				"destinations": free_config.destinations,
				"condition": free_config.condition,
				"value": free_config.condition_value
			})

		return data

	@param_required(['corp_id', 'id', 'name', 'default_config', 'special_configs', 'free_configs',
					 'is_enable_special_config', 'is_enable_free_config'])
	def post(args):
		corp = args['corp']
		name = args['name']
		postage_config_id = args['id']
		is_enable_special_config = (args.get('is_enable_special_config', 'false') == 'true')
		is_enable_free_config = (args.get('is_enable_free_config', 'false') == 'true')
		default_config = json.loads(args.get('default_config', '{}'))
		special_configs = json.loads(args.get('special_configs', '[]'))
		free_configs = json.loads(args.get('free_configs', '[]'))

		postage_config = PostageConfigFactory.get(corp).update({
			'id': postage_config_id,
			'name': name,
			'default_config': default_config,
			'is_enable_special_config': is_enable_special_config,
			'special_configs': special_configs,
			'is_enable_free_config': is_enable_free_config,
			'free_configs': free_configs
		})

		return {
			'id': postage_config_id
		}

	@param_required(['corp_id', 'id'])
	def delete(args):
		corp = args['corp']
		corp.postage_config_repository.delete_postage_config(args['id'])

		return {}

	@param_required(['corp_id', 'name', 'default_config', 'special_configs', 'free_configs',
					 'is_enable_special_config', 'is_enable_free_config'])
	def put(args):
		corp = args['corp']
		name = args['name']
		is_enable_special_config = (args.get('is_enable_special_config', 'false') == 'true')
		is_enable_free_config = (args.get('is_enable_free_config', 'false') == 'true')
		default_config = json.loads(args.get('default_config', '{}'))
		special_configs = json.loads(args.get('special_configs', '[]'))
		free_configs = json.loads(args.get('free_configs', '[]'))

		postage_config = PostageConfigFactory.get(corp).create({
			'name': name,
			'default_config': default_config,
			'is_enable_special_config': is_enable_special_config,
			'special_configs': special_configs,
			'is_enable_free_config': is_enable_free_config,
			'free_configs': free_configs
		})

		return {
			'id': postage_config.id
		}
