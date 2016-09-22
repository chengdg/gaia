# -*- coding: utf-8 -*-

__author__ = 'Eugene'

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product import Product

class AProductStatus(api_resource.ApiResource):
    """
    获取商品的状态
    """
    app = "product"
    resource = "product_status"

    @param_required(['product_ids'])
    def get(args):
        product_ids = args['product_ids'].split("_")
        product_ids = [id for id in product_ids if id]
        # product_ids = json.loads(product_ids)
        products = Product.from_ids({'product_ids': product_ids})
        on_product_ids = Product.check_product_shelve_on({'product_ids': product_ids})
        product_status = []
        for product in products:
            product_status.append({
                    'product_id': product.id,
                    'is_deleted': product.is_deleted,
                    'status': 'on' if product.id in on_product_ids else 'off'
                })
        return {'product_status': product_status}

    @param_required(['product_ids'])
    def post(args):
        product_ids = args['product_ids'].split("_")
        product_ids = [id for id in product_ids if id]

        products = Product.from_ids({'product_ids': product_ids})
        id2created_at = dict([(product.id, product.created_at) for product in products])

        return id2created_at