# -*- coding: utf-8 -*-

from eaglet.core.service.celery import task

import settings
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from db.market_tools.template_message import models as template_message_models

from business.market_tools.template_message.order_template_message_service import OrderTemplageMessageService

@task(bind=True)
def service_send_shiped_order_template_message(self, order_id, webapp_id):
        """
        发货通知模版消息服务

        """
        order_template_message_service = OrderTemplageMessageService.from_webapp_id({
            "webapp_id": webapp_id,
            "send_point": template_message_models.PAY_DELIVER_NOTIFY
            })
        if order_template_message_service:
            order_template_message_service.send_order_templage_message(order_id)    