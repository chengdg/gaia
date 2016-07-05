# -*- coding: utf-8 -*-

__author__ = 'Eugene'

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product import Product

class AProductStatus(api_resource.ApiResource):
    """
    获取商品的状态
    """
    app = "mall"
    resource = "product_status"

    @param_required(['product_ids'])
    def get(args):
        product_ids = args['product_ids'].split("_")
        product_ids = [id for id in product_ids if id]

        products = Product.from_ids({'product_ids': product_ids})
        product_status = []
        for product in products:
            product_status.append({
                    'product_id': product.id,
                    'is_deleted': product.is_deleted
                })
        return {'product_status': product_status}