# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay.pay_interface import PayInterface


class APayInterfaceConfig(api_resource.ApiResource):
    app = 'mall'
    resource = 'pay_interface_config'

    @param_required(['pay_interface_id'])
    def get(args):
        pay_interface_id = args['pay_interface_id']
        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        pay_interface_configs = pay_interface.configs
        return {
            'pay_interface_type': pay_interface.type,
            'pay_interface_name': pay_interface.name,
            'pay_interface_config': pay_interface_configs
        }


    @param_required([])
    def put(args):
        pass

    @param_required([])
    def post(args):
        pass
