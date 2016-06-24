# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.mall.product import Product
from business.account.user_profile import UserProfile

class AOrderList(api_resource.ApiResource):
    """
    订单列表
    """
    app = 'panda'
    resource = 'order_list'

    @param_required(['product_ids'])
    def get(args):
        """
        订单列表
        """
        product_ids = args['product_ids'].split("_")
        product_ids = [id for id in product_ids if id]
        relations = OrderProductRelation.get_for_product({
            'product_ids': product_ids
        })
        order_ids = [relation.order_id for relation in relations]
        orders = Order.from_ids({
            'ids': order_ids
        })
        orders = filter(lambda order: order.origin_order_id > 0, orders)
        orders = AOrderList.search_orders(orders, args)
        #分页
        cur_page = int(args.get('page', '1'))
        count_per_page = int(args.get('count_per_page', '10'))
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page)

        order_ids = [order.id for order in orders]
        relations = filter(lambda relation: relation.order_id in order_ids, relations)
        product_ids = [relation.product_id for relation in relations]
        products = Product.from_ids({'product_ids': product_ids})
        id2product = dict(([product.id, product] for product in products))
        order_id2product_info = {}
        for relation in relations:
            if relation.order_id in order_id2product_info:
                order_id2product_info[relation.order_id].append({
                                        'id': relation.product_id,
                                        'count': relation.number,
                                        'price': relation.price,
                                        'total_price': relation.total_price,
                                        'purchase_price': relation.purchase_price,
                                        'weight': id2product[relation.product_id].weight
                                    })
            else:
                order_id2product_info[relation.order_id] = [{
                                        'id': relation.product_id,
                                        'count': relation.number,
                                        'price': relation.price,
                                        'total_price': relation.total_price,
                                        'purchase_price': relation.purchase_price,
                                        'weight': id2product[relation.product_id].weight
                                    }]
        order_infos = []
        for order in orders:
            order_info = order.to_dict()
            order_info['products'] = order_id2product_info[order.id]
            order_infos.append(order_info)

        return {
            'orders': order_infos,
            'pageinfo': pageinfo.to_dict()
        }

    @staticmethod
    def search_orders(orders=None, args={}):
        # 筛选
        order_id = args.get('order_id', "")
        start_time = args.get('start_time', "")
        end_time = args.get('end_time', "")
        order_status = args.get('status', "")
        webapp_id = args.get('webapp_id', "")

        if order_id:
            orders = filter(lambda order: order.order_id == order_id, orders)
        if order_status:
            orders = filter(lambda order: order.status == int(order_status), orders)
        if webapp_id:
            orders = filter(lambda order: order.webapp_id == webapp_id, orders)
        if start_time and end_time:
            orders = filter(lambda order: order.created_at.strftime('%Y-%m-%d %H:%M:%S') >= start_time and order.created_at.strftime('%Y-%m-%d %H:%M:%S') <= end_time, orders)
        return orders