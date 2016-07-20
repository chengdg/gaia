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


"""
临时性接口不再根据规范来了，怎么块怎么来吧
"""


class AOrderProduct(api_resource.ApiResource):
    """
    脚本需要（临时性接口）查询已经同步的商品产生的订单

    """
    app = 'panda'
    resource = 'order_product'

    @param_required(['product_id'])
    def get(self):
        """
        product_id -- 对应自营平台的自己的商品id

        """
        product_id = json.loads(self.get('product_id'))

        relations = mall_models.OrderHasProduct.select().dj_where(product_id=product_id)
        order_ids = [relation.order_id for relation in relations]

        return {
            'order_ids': order_ids
        }
