# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.product import ProductSales

class AProductSales(api_resource.ApiResource):
    """
    商品的销量
    """
    app = 'panda'
    resource = 'product_sales'

