# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

class OrderStatusLogInfo(business_model.Model):
    """
    订单状态日志
    """
    __slots__ = (
        'logs',
    )

    def __init__(self, order):
        business_model.Model.__init__(self)

        if order:
            self.logs = self.__create_order_log(order)
        else:
            self.logs = []

    @staticmethod
    @param_required(['order'])
    def from_order(args):
        order = args['order']
        return OrderStatusLogInfo(order)

    def __create_order_log(self, order):
        log_models = mall_models.OrderStatusLog.select().dj_where(order_id=order.order_id)
        logs = []
        if order.status == mall_models.ORDER_STATUS_NOT:
            log = {}
            log['status'] = u'已下单'
            log['created_at'] = order.created_at
            log['is_current'] = 0
            logs.append(log)

            log = {}
            log['status'] = u'待支付'
            log['created_at']  = order.created_at
            log['is_current'] = 1
            logs.append(log)

            log = {}
            log['status'] = u'已发货'
            log['created_at']  = ''
            log['is_current'] = 2
            logs.append(log)

            log = {}
            log['status'] = u'交易完成'
            log['created_at']  = ''
            log['is_current'] = 2
            logs.append(log)
        elif order.status in [mall_models.ORDER_STATUS_PAYED_NOT_SHIP, mall_models.ORDER_STATUS_PAYED_SHIPED, mall_models.ORDER_STATUS_SUCCESSED]:
            log = {}
            log['status'] = u'已下单'
            log['created_at'] = order.created_at
            log['is_current'] = 0
            logs.append(log)

            is_current = []
            if order.status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP:
                is_current = [1,2,2]

            if order.status == mall_models.ORDER_STATUS_PAYED_SHIPED:
                is_current = [0,1,2]

            if order.status == mall_models.ORDER_STATUS_SUCCESSED:
                is_current = [0,0,1]

            log = {}
            log['status'] = u'待发货'
            log['created_at']  = order.payment_time
            log['is_current'] = is_current[0]
            logs.append(log)

            log = {}
            log['status'] = u'已发货'
            log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).first() if log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).count()>0 else ''
            log['is_current'] = is_current[1]
            logs.append(log)

            log = {}
            log['status'] = u'交易完成'
            log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).first() if log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).count()>0 else ''
            log['is_current'] = is_current[2]
            logs.append(log)

        elif order.status in [mall_models.ORDER_STATUS_REFUNDING, mall_models.ORDER_STATUS_GROUP_REFUNDING]:
            log = {}
            log['status'] = u'已下单'
            log['created_at'] = order.created_at
            log['is_current'] = 0
            logs.append(log)

            if log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).count() > 0:
                log = {}
                log['status'] = u'交易完成'
                log['created_at']  = log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).first().created_at
                log['is_current'] = 0
                logs.append(log)
            elif log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).count() > 0:
                log = {}
                log['status'] = u'已发货'
                log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).first().created_at
                log['is_current'] = 0
                logs.append(log)
            elif log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
                log = {}
                log['status'] = u'待发货'
                log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP).first().created_at
                log['is_current'] = 0
                logs.append(log)

            log = {}
            log['status'] = u'退款中'
            log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_REFUNDING).first().created_at if log_models.dj_where(to_status=mall_models.ORDER_STATUS_REFUNDING).count() > 0 else ""
            log['is_current'] = 1
            logs.append(log)

            log = {}
            log['status'] = u'退款成功'
            log['created_at']  = ''
            log['is_current'] = 2
            logs.append(log)

        elif order.status in [mall_models.ORDER_STATUS_REFUNDED, mall_models.ORDER_STATUS_GROUP_REFUNDED]:
            log = {}
            log['status'] = u'已下单'
            log['created_at'] = order.created_at
            log['is_current'] = 0
            logs.append(log)

            if log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).count() > 0:
                log = {}
                log['status'] = u'交易完成'
                log['created_at']  = log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).first().created_at
                log['is_current'] = 0
                logs.append(log)
            elif log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).count() > 0:
                log = {}
                log['status'] = u'已发货'
                log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).first().created_at
                log['is_current'] = 0
                logs.append(log)
            elif log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
                log = {}
                log['status'] = u'待发货'
                log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP).first().created_at
                log['is_current'] = 0
                logs.append(log)

            log = {}
            log['status'] = u'退款中'
            log['created_at']  = log_models.dj_where(to_status=mall_models.ORDER_STATUS_REFUNDING).first().created_at if log_models.dj_where(to_status=mall_models.ORDER_STATUS_REFUNDING).count() > 0 else ""
            log['is_current'] = 0
            logs.append(log)

            log = {}
            log['status'] = u'退款成功'
            log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_REFUNDED).first().created_at if log_models.dj_where(to_status=mall_models.ORDER_STATUS_REFUNDED).count() > 0 else ""
            log['is_current'] = 1
            logs.append(log)
        elif order.status == mall_models.ORDER_STATUS_CANCEL:
            log = {}
            log['status'] = u'已下单'
            log['created_at'] = order.created_at
            log['is_current'] = 0
            logs.append(log)

            if log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).count() > 0:
                # if OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
                #   log = {}
                #   log['status'] = u'待发货'
                #   log['created_at'] = OrderStatusLog.objects.filter(order_id=order.order_id,to_status=ORDER_STATUS_PAYED_NOT_SHIP)[0].created_at
                #   log['is_current'] = 0
                #   logs.append(log)
                log = {}
                log['status'] = u'交易完成'
                log['created_at']  = log_models.dj_where(to_status=mall_models.ORDER_STATUS_SUCCESSED).first().created_at
                log['is_current'] = 0
                logs.append(log)

            elif log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP).count() > 0:
                log = {}
                log['status'] = u'待发货'
                log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP).first().created_at
                log['is_current'] = 0
                logs.append(log)
                if log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).count() > 0:
                    log = {}
                    log['status'] = u'已发货'
                    log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_PAYED_SHIPED).first().created_at
                    log['is_current'] = 0
                    logs.append(log)

            log = {}
            log['status'] = u'交易取消'
            log['created_at'] = log_models.dj_where(to_status=mall_models.ORDER_STATUS_CANCEL).first().created_at if log_models.dj_where(to_status=mall_models.ORDER_STATUS_CANCEL) else ""
            log['is_current'] = 1
            logs.append(log)

        return logs

