# -*- coding: utf-8 -*-
from eaglet.core import watchdog
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.mall import models as mall_models


class WZCard(business_model.Model):
    """
    订单
    """

    __slots__ = (

    )

    @staticmethod
    def refund_for_order(order):
        """
        微众卡退款
        """
        # 交易类型（支付失败退款：0、普通退款：1）

        trade_id = mall_models.OrderCardInfo.select().dj_where(order_id=order.order_id).first().trade_id
        data = {
            'trade_id': trade_id,
            'trade_type': 1  # 普通退款
        }

        msg = {
            'uuid': 'refund_wzcard',
            'order_id': order.order_id,
            'weizoom_card_money': order.weizoom_card_money
        }

        watchdog.info(message=msg, log_type='business_log')

        resp = Resource.use('card_apiserver').delete({
            'resource': 'card.trade',
            'data': data
        })

        return resp
