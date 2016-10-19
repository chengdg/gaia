# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

import logging

from bdem import msgutil

from business.mall.corporation import Corporation

from service.service_register import register
from db.express import models as express_models
from zeus_conf import TOPIC


@register("order_applied_for_refunding")
def process(data, recv_msg=None):
	"""
	发货出货单的消息处理
	"""
	pass
	