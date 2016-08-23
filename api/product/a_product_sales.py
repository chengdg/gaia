# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.product_sales import ProductSales

class AProductSales(api_resource.ApiResource):
    """
    商品的销量
    """
    app = 'product'
    resource = 'product_sales'

    @param_required(['product_ids'])
    def get(args):
        product_ids = args.get('product_ids').split("_")
        product_ids = [id for id in product_ids if id]
        sales = ProductSales.from_ids({'product_ids': product_ids})
        product_sales = []
        for sale in sales:
            product_sales.append({
                    'product_id': sale.product_id,
                    'sales': sale.sales
                })
        return {'product_sales': product_sales}