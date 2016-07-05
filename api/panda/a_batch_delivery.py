# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_state import OrderState
from business.tools.express_detail import ExpressDetail

class ABatchDelivery(api_resource.ApiResource):
    """
    订单批量发货
    """
    app = 'panda'
    resource = 'batch_delivery'

    @param_required(['datas'])
    def put(args):
        datas = json.loads(args['datas'])
        order_ids = [data['order_id'] for data in datas]
        orders = OrderState.from_order_ids({'order_ids': order_ids})
        order_id2order = dict([(order.order_id, order) for order in orders])
        response_data = []
        ship_order_ids = []
        for data in datas:
            if data['order_id'] in order_id2order:
                if data['order_id'] in ship_order_ids:
                    response_data.append({
                        'order_id': data['order_id'],
                        'result': False,
                        'msg': u'不能对当前订单发货'
                    })
                    continue
                express_company_name = data['express_company_name']
                express_number = data['express_number']
                operator_name = ''
                leader_name = ''
                result, msg = order_id2order[data['order_id']].ship(express_company_name, express_number, operator_name, leader_name)
                response_data.append({
                        'order_id': data['order_id'],
                        'result': result,
                        'msg': msg
                    })
                ship_order_ids.append(data['order_id'])
            else:
                response_data.append({
                        'order_id': data['order_id'],
                        'result': 'FALUT',
                        'msg': u"订单不存在"
                    })

        return response_data