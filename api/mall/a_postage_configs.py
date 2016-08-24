# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.postage_config import PostageConfig


class APostageConfig(api_resource.ApiResource):
    """
    运费模板集合
    """
    app = 'mall'
    resource = 'postage_configs'

    @param_required(['owner_id'])
    def get(args):
        postage_configs = PostageConfig.from_owner_id({'owner_id': int(args['owner_id'])})
        postage_configs = [postage_config.to_dict() for postage_config in postage_configs]

        return postage_configs