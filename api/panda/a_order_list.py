# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.account.user_profile import UserProfile
from core import paginator


class AOrderList(api_resource.ApiResource):
    """
    订单列表
    """
    app = 'panda'
    resource = 'order_list'

    @param_required(['product_ids', 'account_type'])
    def get(args):
        """
        订单列表
        """
        accout_type = args['account_type']
        product_ids = args['product_ids']

        relations = OrderProductRelation.get_for_product({
            'product_ids': product_ids
        })

        order_ids = [r.order_id for r in relations]
        orders = Order.from_ids({
            'ids': order_ids
        })

        order_id2relation = {}
        for r in relations:
            if r.order_id in order_id2relation:
                order_id2relation[r.order_id].append(r)
            else:
                order_id2relation[r.order_id] = [r]


        # TODO筛选
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


        #分页
        cur_page = args.get('page', 1)
        count_per_page = args.get('count_per_page', 10)
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page)

        if accout_type:
            order_webapp_ids = [order.webapp_id for order in orders]
            user_profiles = UserProfile.from_webapp_ids({
                'webapp_ids': order_webapp_ids
            })

            webapp_id2store_name = dict([(profile.webapp_id, profile.store_name)for profile in user_profiles])

        order_info = []
        for order in orders:
            product_info = []
            order_relations = order_id2relation[order.id]
            for r in order_relations:
                order_money = 0
                product_info.append({
                    'product_id': r.product_id,
                    'total_price': r.total_price,
                    'purchase_price': r.purchase_price,
                    'count': r.number
                })
                order_money += r.total_price
            data = {
                'id': order.id,
                'order_id': order.order_id,
                'created_at': order.created_at,
                'ship_name': order.ship_name,
                'status': order.status,
                'action': "",
                'product_info': product_info,
                'order_money': order_money
            }
            if accout_type:
                data['store_name'] = webapp_id2store_name[order.webapp_id]
            order_info.append(data)

        return {
            'orders': order_info,
            'pageinfo': pageinfo.to_dict()
        }