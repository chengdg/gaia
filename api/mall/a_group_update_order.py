# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from db.mall import models as mall_models
from business.mall.order_has_group import OrderHasGroup
from business.mall.order import Order
from business.mall.order_state import OrderState
from eaglet.core import watchdog

class AGroupUpdateOrder(api_resource.ApiResource):
    """
    团购状态改变处理对应的订单
    """
    app = "mall"
    resource = "group_update_order"

    @param_required(['group_id', 'status'])
    def post(args):
        # watchdog.alert({
        #     'group_id':args['group_id'],
        #     'status':args['status'],
        #     'xid':'xx'
        # },"ONLINE")
        print('-----------xx',args['group_id'],args['status'])
        # return 500,{
        #     'reason':'stop'
        # }

        status = args['status']
        group_id = args['group_id']
        operator_name = args.get('operator_name', "")
        is_test = int(args.get('is_test', 0)) == 1

        if status == 'success':
            group_status = mall_models.GROUP_STATUS_OK
            order_status = mall_models.ORDER_STATUS_NOT
        elif status == 'failure':
            group_status = mall_models.GROUP_STATUS_failure
            order_status = mall_models.ORDER_STATUS_PAYED_NOT_SHIP

        OrderHasGroup.update(group_id, group_status)
        order_ids = OrderHasGroup.get_group_order_ids({'group_id': group_id})
        orders = OrderState.from_order_ids({'order_ids': order_ids})
        if order_status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
            orders = filter(lambda order: order.status in [mall_models.ORDER_STATUS_PAYED_NOT_SHIP, mall_models.ORDER_STATUS_NOT], orders)
        else:
            orders = filter(lambda order: order.status == order_status, orders)
        msg = []
        for order in orders:
            info = ""
            if order_status == mall_models.ORDER_STATUS_NOT:
                info = order.cancel()
            elif order_status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
                if order.pay_interface_type == mall_models.PAY_INTERFACE_WEIXIN_PAY and order.status >= mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
                    if is_test:
                        info = order.refunding()
                        order.updat_status(mall_models.ORDER_STATUS_GROUP_REFUNDING)
                    else:
                        order.refunding()
                        info = order.return_money()
                        order.updat_status(mall_models.ORDER_STATUS_GROUP_REFUNDING)
                else:
                    info = order.cancel()
            msg.append(info)
        return {"msg": msg}