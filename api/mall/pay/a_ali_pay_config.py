# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay.pay_interface import PayInterface


class AAliPayConfig(api_resource.ApiResource):
    """
    微信支付的支付接口
    """
    app = 'mall'
    resource = 'ali_pay_config'

    @param_required(['corp_id', 'version'])
    def post(args):
        """
        @param args: owner_id--->用户id
                     id---->支付方式的id
                     is_enable-->是否启用支付方式
        @return:
        """
        corp = args['corp']
        ali_pay_interface = corp.pay_interface_repository.get_ali_pay_interface()
        ali_pay_interface.update_config(args)

        if 'is_active' in args:
            if args['is_active'] == 'true':
                ali_pay_interface.enable()
            else:
                ali_pay_interface.disable()

        return {}
