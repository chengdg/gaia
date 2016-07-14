# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_factory import ProductFactory
from business.mall.product import Product


class AProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "mall"
    resource = "product"

    @param_required(['name', 'supplier', 'model_type', 'stock_type', 'images', 'product_id', 'purchase_price'])
    def put(self):
        """
        同步商品（添加商品）
        product_id -- panda系统商品的id
        name -- 商品名称
        supplier -- 供货商id（同步过来的供货商id）
        model_type -- 规格类型 single： 默认单规格,
                        ;custom: 定制规格（此时必须传递规格信息参数）
        stock_type -- 库存类型limit:有限(1) unbound: 无限(0)
        images -- 商品路播图[{order:1, url: url}]
        purchase_price -- 进价


        --------------非必须------------------
        stocks -- 库存数量
        detail -- 商品详情
        price -- 价格（单品）
        weight -- 重量（单品）
        model_info -- 规格信息
        """
        #
        factory = ProductFactory.create()
        try:
            product = factory.save(args=self)
            return {
                'product': product.to_dict(),
                'models': product.models

            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                'product': None
            }
