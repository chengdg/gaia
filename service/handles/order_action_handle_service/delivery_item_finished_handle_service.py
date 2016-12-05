# -*- coding: utf-8 -*-
"""
已完成
"""


# -*- coding: utf-8 -*-
"""
处理订单的消息service(演示)

@author Victor
"""

# import logging
#
# from bdem import msgutil
#
# from business.mall.corporation import Corporation
# from business.mall.express.express_service import ExpressService
# from business.mall.express.kdniao_express_poll import KdniaoExpressPoll
# from service.handler_register import register
# from db.express import models as express_models
# from gaia_conf import TOPIC
# from service.utils import not_retry
#
#
# @register("delivery_item_finished")
# @not_retry
# def process(data, recv_msg=None):
# 	"""
# 	发货出货单的消息处理
# 	"""
#
# 	corp_id = data['corp_id']
# 	delivery_item_id = data['delivery_item_id']
# 	to_status = data['to_status']
#
# 	# 发送通知邮件
# 	topic_name = TOPIC['base_service']
# 	data = {
# 		"type": "delivery_item",
# 		"delivery_item_id": delivery_item_id,
# 		"corp_id": corp_id
# 	}
# 	msgutil.send_message(topic_name, 'send_order_email_task', data)
