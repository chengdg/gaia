# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.account.user_profile import UserProfile

class AOrderList(api_resource.ApiResource):
    """
    订单列表
    """
    app = 'mall'
    resource = 'order_list'

    @param_required(['product_ids'])
    def get(args):
        """
        订单列表
        """
        accout_type = args['account_type']
        product_ids = args['product_ids'].split("_")

        relations = OrderProductRelation.get_for_product({
            'product_ids': product_ids
        })

        order_ids = [r.order_id for r in relations if r.order.origin_order_id > 0]
        orders = Order.from_ids({
            'ids': order_ids
        })

        orders = AOrderList.search_orders(orders, args)

        #分页
        cur_page = args.get('page', 1)
        count_per_page = args.get('count_per_page', 10)
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page)

        return {
            'orders': orders,
            'pageinfo': pageinfo.to_dict()
        }

    @staticmethod
    def search_orders(orders=None, args={}):
        # 筛选
        order_id = args.get('order_id', "")
        start_time = args.get('start_time', "")
        end_time = args.get('end_time', "")
        order_status = args.get('status', "")

        if order_id:
            orders = filter(lambda order: order.order_id == order_id, orders)
        if order_status:
            orders = filter(lambda order: order.status == order_status, orders)
        if start_time and end_time:
            orders = filter(lambda order: order.created_at >= start_time and order.created_at <= end_time, orders)
        return orders