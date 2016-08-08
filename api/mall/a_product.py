# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_factory import ProductFactory
from business.mall.product import Product, ProductModel, ProductSwipeImage, ProductPool
from settings import PANDA_IMAGE_DOMAIN


class AProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "mall"
    resource = "product"

    @param_required([])
    def put(args):
        """
        创建商品
        @return:
        """
        product_factory = ProductFactory.create()
        product_factory.create_product(args)
        return {}



    @param_required([])
    def post(args):
        pass

