# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay.pay_interface import PayInterface


class APayInterface(api_resource.ApiResource):
    """
    单个支付方式
    """
    app = 'mall'
    resource = 'pay_interface'

    @param_required(['owner_id', 'id'])
    def get(args):
        return {}

    @param_required([])
    def put(args):
        return {}

    @param_required(['owner_id', 'id', 'is_enable'])
    def post(args):
        """

        @param args: owner_id--->用户id
                     id---->支付方式的id
                     is_enable-->是否启用支付方式
        @return:
        """
        owner_id = int(args['owner_id'])
        pay_interface_id = args['id']
        is_enable = True if args['is_enable'] == 'true' else False

        try:
            pay_interface = PayInterface.from_id({'id': pay_interface_id})
            if owner_id == pay_interface.owner_id:
                pay_interface.update_status(is_enable=is_enable)
                return {'msg': 'success'}
            else:
                return 500, {'msg': "failed"}
        except:
            return 500, {'msg': "failed"}


    @param_required([])
    def delete(args):
        return {}
