# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.product_sales import ProductSales

class AProductSales(api_resource.ApiResource):
    """
    商品的销量
    """
    app = 'mall'
    resource = 'product_sales'

    @param_required(['product_ids'])
    def get(args):
        product_ids = args.get('product_ids').split("_")
        sales = ProductSales.from_ids({'product_ids': product_ids})
        product_sales = {}
        for sale in sales:
            product_sales[sale.product_id] = sale.sales
        return product_sales