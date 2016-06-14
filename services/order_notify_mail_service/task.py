# -*- coding: utf-8 -*-

from eaglet.core.service.celery import task

import settings
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from business.mall.order_email_service import OrderEmailService


@task(bind=True)
def service_send_order_email(self, order_id, webapp_id, status):
        """
        发送邮件，通知订单消息
        """
        email_service = OrderEmailService.from_status({
            "webapp_id": webapp_id,
            "status": status
            })
        if email_service:
            email_service.send_message(order_id)        
