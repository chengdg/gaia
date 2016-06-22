# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AGroupUpdateOrder(api_resource.ApiResource):
    """
    团购状态改变处理对应的订单
    """

    @param_required(['group_id', 'status', 'order_ids', 'is_test'])
    def post(args):
        status = args['status']
        group_id = args['group_id']
        order_ids = json.loads(args['order_ids'])
        is_test = args['is_test']

        if status == 'success':
            group_status = GROUP_STATUS_OK
            order_status = ORDER_STATUS_NOT
        elif status == 'failure':
            group_status = GROUP_STATUS_failure
            order_status = ORDER_STATUS_PAYED_NOT_SHIP