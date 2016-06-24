# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from db.mall import models as mall_models
from business.mall.order_has_group import OrderHasGroup
from business.mall.order import Order
from business.mall.order_state import OrderState

class AGroupUpdateOrder(api_resource.ApiResource):
    """
    团购状态改变处理对应的订单
    """
    app = "mall"
    resource = "group_update_order"

    @param_required(['group_id', 'status'])
    def post(args):
        status = args['status']
        group_id = args['group_id']
        operator_name = args.get('operator_name', "")
        is_test = args.get('is_test', True)

        if status == 'success':
            group_status = GROUP_STATUS_OK
            order_status = ORDER_STATUS_NOT
        elif status == 'failure':
            group_status = GROUP_STATUS_failure
            order_status = ORDER_STATUS_PAYED_NOT_SHIP

        OrderHasGroup.update(group_id, group_status)
        order_ids = OrderHasGroup.get_group_order_ids({'group_id': group_id})
        orders = OrderState.from_order_ids({'order_ids': order_ids})
        if order_status == ORDER_STATUS_PAYED_NOT_SHIP:
            orders = filter(lambda order: order.status in [ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_NOT], orders)
        else:
            orders = filter(lambda order: order.status == order_status, orders)
        msg = ""
        for order in orders:
            msg = ""
            if order_status == ORDER_STATUS_NOT:
                msg = order.cancel()
            elif order_status == ORDER_STATUS_PAYED_NOT_SHIP:
                if order.pay_interface_type == PAY_INTERFACE_WEIXIN_PAY and order.status >= ORDER_STATUS_PAYED_NOT_SHIP:
                    if is_test:
                        order.refund()
                        order.updat_status(mall_models.ORDER_STATUS_GROUP_REFUNDING)
                    else:
                        order.refund()
                        order.return_money()
                else:
                    msg = order.cancel()
        return {"msg": msg}