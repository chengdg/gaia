# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

class OrderOperationLogInfo(business_model.Model):
    """
    订单操作日志
    """

    __slots__ = {
        'order_id',
        'action',
        'operator',
        'created_at',
        'leader_name'
    }

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['order', 'child_orders'])
    def from_order(args):
        order = args['order']
        child_orders = args['child_orders']

        if len(child_orders) == 1:
            models = mall_models.OrderOperationLog.select().dj_where(order_id=order.order_id)
        else:
            models = mall_models.OrderOperationLog.select().where(mall_models.OrderOperationLog.order_id.contains(order.order_id))
            # TODO 进一步筛选

        logs = []
        print models
        for model in models:
            logs.append(OrderOperationLogInfo(model).to_dict())
        for log in logs:
            log['leader_name'] = order.leader_name
            for child_order in child_orders:
                if child_order.order_id == log['order_id']:
                    log['leader_name'] = child_order.leader_name
        logs.append(log)
        return logs