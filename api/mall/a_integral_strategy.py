# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AIntegralStrategy(api_resource.ApiResource):
    """
    积分规则设置
    """
    app = 'mall'
    resource = 'integral_strategy'

    @param_required(['webapp_id'])
    def get(args):
        pass

    @param_required(['webapp_id'])
    def post(args):
        pass