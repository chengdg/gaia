# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay.pay_interface import PayInterface


class AWeixinPayInterface(api_resource.ApiResource):
    """
    微信支付的支付接口
    """
    app = 'mall'
    resource = 'weixin_pay_interface'

    @param_required(['corp_id', 'id', 'is_active'])
    def post(args):
        """
        @param args: owner_id--->用户id
                     id---->支付方式的id
                     is_enable-->是否启用支付方式
        @return:
        """
        corp = args['corp']
        weixin_pay_interface = corp.pay_interface_repository.get_weixin_pay_interface(args['id'])
        weixin_pay_interface.update_config(args)

        if args['is_active'] == 'true':
            weixin_pay_interface.enable()
        else:
            weixin_pay_interface.disable()

        return {}


    @param_required([])
    def delete(args):
        return {}
