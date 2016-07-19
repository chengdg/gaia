# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.mall.product import Product
from business.mall.order_has_group import OrderHasGroup
from db.mall import models as mall_models
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
        orders = AOrderList.filter_group_order(orders)
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

    @staticmethod
    def filter_group_order(orders=None):
        """
        去除团购不显示的订单
        """
        group_relations = OrderHasGroup.from_order_ids({
                                'order_ids': [order.order_id for order in orders]
                            })
        group_order_ids = [r.order_id for r in group_relations]
        order_id2group_relation = dict([(r.order_id, r) for r in group_relations])
        filter_order_ids = []
        for order in orders:
            if order.status == mall_models.ORDER_STATUS_NOT and order.order_id in group_order_ids:
                filter_order_ids.append(order.order_id)
            if order.status == mall_models.ORDER_STATUS_PAYED_NOT_SHIP \
            and order.order_id in group_order_ids \
            and order_id2group_relation[order.order_id].group_status in [mall_models.GROUP_STATUS_ON, mall_models.GROUP_STATUS_failure]:
                filter_order_ids.append(order.order_id)
            if order.status == mall_models.ORDER_STATUS_CANCEL \
            and order.order_id in group_order_ids \
            and order_id2group_relation[order.order_id].group_status in [mall_models.GROUP_STATUS_OK, mall_models.GROUP_STATUS_failure]:
                filter_order_ids.append(order.order_id)

        orders = filter(lambda order: order.order_id not in filter_order_ids, orders)
        orders = sorted(orders, key = lambda order: order.id, reverse=True)
        return orders

    @param_required(['page', 'per_count_page'])
    def post(self):
        """
        page -- 页码
        per_count_page -- 一页多少记录
        ----------------option--------
        product_ids -- 云上通的商品id集合（panda已经处理过映射关系）[id,id]
        supplier_ids -- 云上通的供货商id(panda已经处理过映射关系）[id,id]
        from_mall -- 哪个自营平台（自营平台id,已经通过配置拿到了云上通对应的id)
        order_create_start -- 下单时间区间start
        order_create_end -- 下单时间区间end
        order_status -- 订单状态
        """
        page = self.get('page', 1)
        per_count_page = self.get('per_count_page', 15)

        product_ids = self.get('product_ids')
        supplier_ids = self.get('supplier_ids')
        from_mall = self.get('from_mall')
        order_create_start = self.get('order_create_start')
        order_create_end = self.get('order_create_end')
        order_status = self.get('order_status')

        Order.from_product_ids()
