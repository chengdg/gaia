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
        postage_config = PostageConfig.get({
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
        PostageConfig.update(args)
        return {}

    @param_required(['id', 'owner_id'])
    def delete(args):
        PostageConfig.delete({'id': args['id'], 'owner_id': args['owner_id']})
        return {}

    @param_required([])
    def put(args):
        PostageConfig.create(args)
        return {}



