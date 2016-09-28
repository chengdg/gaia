# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.mall_config import MallConfig


class AConfig(api_resource.ApiResource):
    app = 'mall'
    resource = 'config'

    @param_required(['corp'])
    def get(args):
        mall_config = args['corp'].mall_config

        pay_interfaces = mall_config.pay_interfaces
        
        woid = args['woid']
        mall_config = MallConfig.get({'woid': woid})

        return {
            'mall_config': mall_config.to_dict()
        }

    @param_required(['woid'])
    def post(args):
        try:
            mall_config = MallConfig.set(args)
            return {'mall_config': mall_config.to_dict()}
        except:
            return 500, {}
