# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay.pay_interface import PayInterface


class APayInterfaceActivity(api_resource.ApiResource):
    """
    支付方式启用状态
    """
    app = 'mall'
    resource = 'pay_interface_activity'

    @param_required(['corp_id', 'id', 'is_active'])
    def post(args):
        """
        @param args:
                     id---->支付方式的id
                     is_enable-->是否启用支付方式
        @return:
        """
        corp = args['corp']
        pay_interface = corp.pay_interface_repository.get_pay_interface(args['id'])
        if args['is_active'] == 'true':
            pay_interface.enable()
        else:
            pay_interface.disable()

        return {}
