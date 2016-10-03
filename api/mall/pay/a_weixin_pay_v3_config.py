# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AWeixinPayV3Config(api_resource.ApiResource):
    """
    微信支付v3版的配置
    """
    app = 'mall'
    resource = 'weixin_pay_v3_config'

    @param_required(['corp_id', 'app_id', 'mch_id', 'api_key', 'paysign_key'])
    def post(args):
        """
        """
        corp = args['corp']
        weixin_pay_interface = corp.pay_interface_repository.get_weixin_pay_interface()
        weixin_pay_interface.update_v3_config(args)

        if 'is_active' in args:
            if args['is_active'] == 'true':
                weixin_pay_interface.enable()
            else:
                weixin_pay_interface.disable()

        return {}
