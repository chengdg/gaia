# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.postage_config import PostageConfig


class APostageConfig(api_resource.ApiResource):
	"""
	运费模板
	"""
	app = 'mall'
	resource = 'postage_config'

	@param_required(['id', 'owner_id'])
	def get(args):
		postage_config = PostageConfig.from_id({
			'id': int(args['id']),
			'owner_id': int(args['owner_id'])
		})

		return {
			'special_configs': postage_config.special_configs,
			'free_configs': postage_config.free_configs,
			'postage_config': postage_config.config
		}

	@param_required([])
	def post(args):
		id = args['id']
		owner_id = args['owner_id']
		is_used = args.get('is_used', None)
		name = args.get('name', None)

		if is_used and not name:
			PostageConfig.enable({'id': id, 'owner_id': owner_id})
		else:
			PostageConfig.modify({
				'id': id,
				'owner_id': args['owner_id'],
				'name': args['name'],
				'first_weight': args['first_weight'],
				'first_weight_price': args['first_weight_price'],
				'added_weight': args['added_weight'],
				'added_weight_price': args['added_weight_price'],
				'is_enable_special_config': args['is_enable_special_config'],
				'special_configs': args.get('special_configs', []),
				'is_enable_free_config': args['is_enable_free_config'],
				'free_configs': args.get('free_configs', [])
			})

		return {}

	@param_required(['id', 'owner_id'])
	def delete(args):
		PostageConfig.delete({'id': args['id'], 'owner_id': args['owner_id']})
		return {}

	@param_required(['owner_id', 'name', 'first_weight', 'first_weight_price', 'added_weight', 'added_weight_price',
	                 'is_enable_special_config', 'is_enable_free_config'])
	def put(args):
		PostageConfig.create({
			'owner_id': args['owner_id'],
			'name': args['name'],
			'first_weight': args['first_weight'],
			'first_weight_price': args['first_weight_price'],
			'added_weight': args['added_weight'],
			'added_weight_price': args['added_weight_price'],
			'is_enable_special_config': args['is_enable_special_config'],
			'special_configs': args.get('special_configs', []),
			'is_enable_free_config': args['is_enable_free_config'],
			'free_configs': args.get('free_configs', [])
		})
		return {}
