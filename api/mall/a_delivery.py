# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_state import OrderState


class ADelivery(api_resource.ApiResource):
    """
    发货
    """
    app = 'mall'
    resource = 'delivery'

    @param_required(['order_id'])
    def put(args):
        """
        订单详情
        """
        order_id = args.get('order_id')
        express_company_name = args.get('express_company_name', '')
        express_number =args.get('express_number', '')

        leader_name = args.get('leader_name', '')
        #is_100 = False if str(args.get('is_100', '0')) == "0" else True
        operator_name = args.get('operator_name', '')

        order = OrderState.from_order_id({'order_id': args['order_id']})
        if not order:
            return {
                'result': 'FAILED',
                'msg': u"订单不存在"
            }
        
        result, msg = order.ship(express_company_name, express_number, operator_name, leader_name)

        if result:
            result = "SUCCESS"
        else:
            result = "FAILED"
        return {
            'result': result,
            'msg': msg
        }

    @param_required(['order_id'])
    def post(args):
        order_id = args.get('order_id')
        express_company_name = args.get('express_company_name', '')
        express_number =args.get('express_number', '')

        leader_name = args.get('leader_name', '')
        #is_100 = False if str(args.get('is_100', '0')) == "0" else True
        operator_name = args.get('operator_name', '')
        is_update_express = args.get("is_update_express", "0")

        order = OrderState.from_order_id({'order_id': args['order_id']})
        if not order:
            return {
                'result': 'FALUT',
                'msg': u"订单不存在"
            }
        
        result, msg = order.update_ship(express_company_name, express_number, operator_name, leader_name)
        
        if result:
            result = "SUCCESS"
        else:
            result = "FALUT"
        return {
            'result': result,
            'msg': msg
        }
