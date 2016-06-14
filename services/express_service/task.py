# -*- coding: utf-8 -*-

from eaglet.core.service.celery import task

import settings
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from business.mall.express.express_service import ExpressService
from business.mall.order import Order


@task(bind=True)
def service_express(self, order_id):
        """
        订阅快递信息
        """
        order = Order.from_order_id({
            "order_id": order_id
            })
        if order:
            ExpressService(order).get_express_poll() 