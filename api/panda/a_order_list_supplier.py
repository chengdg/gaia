# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.product.product import Product
from business.mall.order_has_group import OrderHasGroup
from business.mall.product_model_property_value import ProductModelPropertyValue
from db.mall import models as mall_models
from business.account.user_profile import UserProfile

class AOrderListBySupplier(api_resource.ApiResource):
    """
    订单列表
    """
    app = 'panda'
    resource = 'order_list_by_supplier'

    @param_required(['supplier_ids'])
    def get(args):
        """
        订单列表
        """
        supplier_ids = args['supplier_ids'].split("_")
        supplier_ids = [id for id in supplier_ids if id]
        product_ids = args.get('product_ids', "")
        product_ids = product_ids.split("_") if product_ids else []
        product_ids = [id for id in product_ids if id]

        if supplier_ids:
            orders = Order.from_suppliers({
                    'supplier_ids': supplier_ids
                })
        if product_ids:
            relations = OrderProductRelation.get_for_product({
                'product_ids': product_ids
            })
            order_ids = [relation.order_id for relation in relations]
            orders = Order.from_ids({
                'ids': order_ids
            })
            orders = filter(lambda order: order.origin_order_id > 0, orders)

        orders = AOrderListBySupplier.filter_group_order(orders)
        orders = AOrderListBySupplier.search_orders(orders, args)
        #分页
        cur_page = int(args.get('page', '1'))
        count_per_page = int(args.get('count_per_page', '10'))
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page)

        order_ids = [order.id for order in orders]
        if order_ids:
            relations = OrderProductRelation.get_for_order({'order_ids': order_ids})
        else:
            relations = []
        product_ids = [relation.product_id for relation in relations]
        products = Product.from_ids({'product_ids': product_ids})
        id2product = dict(([product.id, product] for product in products))
        order_id2product_info = {}
        #商品规格
        product_model_names = [relation.product_model_name for relation in relations if relation.product_model_name != 'standard']
        model_value_ids = []
        model_property_ids = []
        for product_model_name in product_model_names:
            for model_name in product_model_name.split('_'):
                model_value_ids.append(int(model_name.split(':')[1]))
                model_property_ids.append(int(model_name.split(':')[0]))

        product_property_values = ProductModelPropertyValue.from_ids_and_property_ids({
                'ids': model_value_ids,
                'property_ids': model_property_ids
            })
        product_model_value2name = dict([('%d:%d' % (product_property_value.property_id, product_property_value.id), product_property_value.name) for product_property_value in product_property_values])

        for relation in relations:
            product_model_name = relation.product_model_name
            model_names = []
            if product_model_name != 'standard':
                for model_name in product_model_name.split('_'):
                    model_names.append(product_model_value2name[model_name])

            if relation.order_id in order_id2product_info:
                order_id2product_info[relation.order_id].append({
                                        'id': relation.product_id,
                                        'count': relation.number,
                                        'price': relation.price,
                                        'total_price': relation.total_price,
                                        'purchase_price': relation.purchase_price,
                                        'weight': id2product[relation.product_id].weight,
                                        'model_names': model_names
                                    })
            else:
                order_id2product_info[relation.order_id] = [{
                                        'id': relation.product_id,
                                        'count': relation.number,
                                        'price': relation.price,
                                        'total_price': relation.total_price,
                                        'purchase_price': relation.purchase_price,
                                        'weight': id2product[relation.product_id].weight,
                                        'model_names': model_names
                                    }]
        order_infos = []
        for order in orders:
            order_info = order.to_dict()
            if not order_id2product_info.has_key(order.id):
                continue
            order_info['products'] = order_id2product_info[order.id]
            order_infos.append(order_info)

        return {
            'orders': order_infos,
            'pageinfo': pageinfo.to_dict()
        }

    @param_required(['supplier_ids'])
    def post(args):
        """
        订单列表
        """
        supplier_ids = args['supplier_ids'].split("_")
        supplier_ids = [id for id in supplier_ids if id]
        product_ids = args.get('product_ids', "")
        product_ids = product_ids.split("_") if product_ids else []
        product_ids = [id for id in product_ids if id]

        if supplier_ids:
            orders = Order.from_suppliers({
                    'supplier_ids': supplier_ids
                })
        if product_ids:
            relations = OrderProductRelation.get_for_product({
                'product_ids': product_ids
            })
            order_ids = [relation.order_id for relation in relations]
            orders = Order.from_ids({
                'ids': order_ids
            })
            orders = filter(lambda order: order.origin_order_id > 0, orders)

        orders = AOrderListBySupplier.filter_group_order(orders)
        orders = AOrderListBySupplier.search_orders(orders, args)
        #分页
        cur_page = int(args.get('page', '1'))
        count_per_page = int(args.get('count_per_page', '10'))
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page)

        order_ids = [order.id for order in orders]
        if order_ids:
            relations = OrderProductRelation.get_for_order({'order_ids': order_ids})
        else:
            relations = []
        product_ids = [relation.product_id for relation in relations]
        products = Product.from_ids({'product_ids': product_ids})
        id2product = dict(([product.id, product] for product in products))
        order_id2product_info = {}
        #商品规格
        product_model_names = [relation.product_model_name for relation in relations if relation.product_model_name != 'standard']
        model_value_ids = []
        model_property_ids = []
        for product_model_name in product_model_names:
            for model_name in product_model_name.split('_'):
                model_value_ids.append(int(model_name.split(':')[1]))
                model_property_ids.append(int(model_name.split(':')[0]))

        product_property_values = ProductModelPropertyValue.from_ids_and_property_ids({
                'ids': model_value_ids,
                'property_ids': model_property_ids
            })
        product_model_value2name = dict([('%d:%d' % (product_property_value.property_id, product_property_value.id), product_property_value.name) for product_property_value in product_property_values])

        for relation in relations:
            product_model_name = relation.product_model_name
            model_names = []
            if product_model_name != 'standard':
                for model_name in product_model_name.split('_'):
                    model_names.append(product_model_value2name[model_name])
            if relation.order_id in order_id2product_info:
                order_id2product_info[relation.order_id].append({
                                        'id': relation.product_id,
                                        'name': id2product[relation.product_id].name,
                                        'thumbnails_url': id2product[relation.product_id].thumbnails_url,
                                        'count': relation.number,
                                        'price': relation.price,
                                        'total_price': relation.total_price,
                                        'purchase_price': relation.purchase_price,
                                        'weight': id2product[relation.product_id].weight,
                                        'model_names': model_names
                                    })
            else:
                order_id2product_info[relation.order_id] = [{
                                        'id': relation.product_id,
                                        'name': id2product[relation.product_id].name,
                                        'thumbnails_url': id2product[relation.product_id].thumbnails_url,
                                        'count': relation.number,
                                        'price': relation.price,
                                        'total_price': relation.total_price,
                                        'purchase_price': relation.purchase_price,
                                        'weight': id2product[relation.product_id].weight,
                                        'model_names': model_names
                                    }]
        order_infos = []
        for order in orders:
            order_info = order.to_dict()
            if not order_id2product_info.has_key(order.id):
                continue
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

        orders = filter(lambda order: (order.status in [3,4,5,6,7]) or (order.status == 1 and order.payment_time.strftime('%Y-%m-%d %H:%M:%S') > "2000-01-01 00:00:00"), orders)
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