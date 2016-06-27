# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_factory import ProductFactory

class AProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "mall"
    resource = "product"

    @param_required([])
    def put(args):
        product_factory = ProductFactory.get()
        product_model = product_factory.create_product(args)