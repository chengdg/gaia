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
    def empty_order_operation_log_info(model=None):
        order_operation_log_info = OrderOperationLogInfo(model)
        return order_operation_log_info

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

    @staticmethod
    @param_required(['order_id'])
    def from_order_id(args):
        order_operation_logs = mall_models.OrderOperationLog.select().dj_where(order_id=args['order_id'])
        return [OrderOperationLogInfo(order_operation_log) for order_operation_log in order_operation_logs]

    def get_orders_operation(self, orders, start_time=None, end_time=None, action=None):
        print start_time, end_time, action
        if start_time and end_time and action:
            order_operation_logs = mall_models.OrderOperationLog.filter(created_at__gte=start_time, created_at__lt=end_time, action=action)
            order_ids_in_delivery_intervale = [x.order_id for x in order_operation_logs]
            return order_ids_in_delivery_intervale
        else:
            return None

    def  from_order_id_action(self, order_id, action):
        order_operation_logs = mall_models.OrderOperationLog.select().dj_where(order_id=order_id, action=action)
        if order_operation_logs.first():
            return OrderOperationLogInfo(order_operation_logs.first())
        else:
            return None

