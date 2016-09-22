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
from eaglet.core.cache import utils as cache_util
from db.mall import models as mall_models
from eaglet.core import watchdog
from business import model as business_model
from business.product.product import Product
from supplier import Supplier
from business.account.user_profile import UserProfile
from order_has_promotion import OrderHasPromotion
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
        order_product_ids = [r.product_id for r in order_product_relations]
        order_products = Product.from_ids({'product_ids': order_product_ids})

        supplier_ids = []
        supplier_user_ids = []
        id2product = {}
        for product in order_products:
            id2product[product.id] = product
            if product.supplier:
                supplier_ids.append(product.supplier)
            if product.supplier_user_id:
                supplier_user_ids.append(product.supplier_user_id)

        id2supplier_name = Supplier.get_id_2_supplier_name({'ids': supplier_ids})
        id2store_name = UserProfile.get_user_id_2_store_name({'user_ids': supplier_user_ids})

        # 订单和促销的关系
        order_promotion_relations = OrderHasPromotion.from_order({'order_id': order.id})
        id2promotion = dict([(r.id, r)for r in order_promotion_relations])
        product2integral = dict([
                                (relation.promotion_result.get('integral_product_info'), relation)
                                for relation in order_promotion_relations
                            ])

        products = []
        pricecut_id = None
        # 当前促销id
        current_promotion_id = None
        # 当前促销第一个主商品
        promotion_first_product = None
        # 当前促销买赠商品
        temp_premium_products = []
        for relation in order_product_relations:
            order.product_count += relation.number
            product = id2product[relation.product_id]
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
                'purchase_price': relation.purchase_price,
                'weight': product.weight
            }

            # 处理商品促销
            promotion_relation = id2promotion.get(relation.promotion_id, None)
            if promotion_relation:
                promotion_result = promotion_relation.promotion_result
                product_info['promotion'] = promotion_result

                # 处理订单详情页跨行的问题
                if current_promotion_id != relation.promotion_id:
                    # 当前促销中第一个主商品
                    # 设定当前促销变量
                    current_promotion_id = relation.promotion_id
                    promotion_first_product = product_info

                    if len(temp_premium_products) > 0:
                        # 上一个促销有赠品
                        products.extend(temp_premium_products)
                        temp_premium_products = []
                    # 初始跨行值为1
                    product_info['rowspan'] = 1
                    if promotion_result['type'] == 'premium_sale':
                        # 买赠商品主商品跨行数+赠品数
                        if promotion_result.has_key('premium_products'):
                            product_info['rowspan'] += len(promotion_result['premium_products'])

                            # 当前促销第一个主商品处理赠品信息
                            for premium_product in promotion_relation.promotion_result['premium_products']:
                                temp_premium_products.append({
                                    "id": premium_product['id'],
                                    "name": premium_product['name'],
                                    "thumbnails_url": premium_product['thumbnails_url'],
                                    "count": premium_product['count'],
                                    "price": '%.2f' % premium_product['price'],
                                    "total_price": '0.0',
                                    'product_model_name': "standard",
                                    "promotion": {
                                        "type": "premium_sale:premium_product"
                                    },
                                    'noline': 1,
                                    'supplier': product.supplier,
                                    'supplier_user_id': product.supplier_user_id,
                                    'user_code':product.user_code
                                })
                else:
                    # 当前促销中其余商品 不显示上边框,给主商品跨行+1
                    product_info['noline'] = 1
                    promotion_first_product['rowspan'] += 1
            else:
                if len(temp_premium_products) > 0:
                    products.extend(temp_premium_products)
                    temp_premium_products = []
                product_info['promotion'] = None

            products.append(product_info)
            if len(temp_premium_products) > 0:
                # 最后一个促销有赠品
                products.extend(temp_premium_products)

        self.products = products
