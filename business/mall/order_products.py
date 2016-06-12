# -*- coding: utf-8 -*-
"""@package business.mall.order_products
订单商品(OrderPdocut)集合

OrderProducts用于构建一组OrderProduct，OrderProducts存在的目的是为了后续优化，以最少的数据库访问次数对商品信息进行批量填充

"""

import json
from bs4 import BeautifulSoup
import math
import itertools

from eaglet.decorator import param_required
#from wapi import wapi_utils
from eaglet.core.cache import utils as cache_util
from db.mall import models as mall_models
from eaglet.core import watchdog
from business import model as business_model
from product import Product
import settings


class OrderProducts(business_model.Model):
    """订单商品集合
    """
    __slots__ = (
        'products',
    )


    @staticmethod
    @param_required(['order'])
    def get_for_order(args):
        """
        获取订单的商品信息
        """
        order_products = OrderProducts()
        order_products.__get_products_for_order(args['order'])

        return order_products

    def __init__(self):
        business_model.Model.__init__(self)

    def __get_products_for_order(self, order):
        '''
        根据order获取订单商品集合
        '''
        # 订单和商品的关系
        order_product_relations = mall_models.OrderHasProduct.select().dj_where(order=order.id)
        # order_product_ids = [r.product_id for r in order_product_relations]

        # # 订单和促销的关系
        # order_promotion_relations = mall_models.OrderHasPromotion.select().dj_where(order=order.order_id)
        # id2promotion = dict([(r.id, r)for r in order_promotion_relations])

        products = []
        pricecut_id = None
        # 当前促销id
        current_promotion_id = None
        # 当前促销第一个主商品
        promotion_first_product = None
        # 当前促销买赠商品
        temp_premium_products = []
        suppliers = []
        supplier_user_ids = []
        for relation in order_product_relations:
            product = Product.from_id({'product_id': relation.product_id})
            product.fill_specific_model(relation.product_model_name)

            product_info = {
                'id' : product.id,
                'name': product.name,
                'thumbnails_url': product.thumbnails_url,
                'count': relation.number,
                'total_price': '%.2f' % relation.total_price,
                'price': '%.2f' % (relation.total_price / relation.number),
                'custom_model_properties': product.custom_model_properties,
                'product_model_name': product.model_name,
                'physical_unit': product.physical_unit,
                'is_deleted': product.is_deleted,
                'grade_discounted_money': relation.grade_discounted_money,
                'supplier': product.supplier,
                'supplier_user_id': product.supplier_user_id,
                'user_code':product.user_code,
                'purchase_price': relation.purchase_price

            }
            products.append(product_info)
            # TODO 有关商品供货商的信息


        print ">>>>S>SS>S>S>S>S>S>",products
        self.products = products
