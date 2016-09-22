# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.decorator import param_required

from business.product.product import Product


class AProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "panda"
    resource = "product_store"

    @param_required(['product_id', 'model_info', 'model_type'])
    def post(self):
        """
        model_info : [{name:name, product_store:product_store}] 单品只许传递一个，standard
        model_type: single 单品
        """
        model_type = self.get('model_type', None)
        if not model_type:
            return {
                'SUCCESS': False
            }
        product_id = self.get('product_id')
        model_info = json.loads(self.get('model_info'))

        product = Product.from_id({'product_id': product_id})
        try:
            if model_type == 'single':
                # 单规格
                standard_model_property = model_info[0]

                # 有限
                if product.stock_type != 1:
                    product.stock_type = 1
                    product.update()
                product_models = ProductModel.from_product_id({'product_id': product_id})

                standard_product_model = None
                for product_model in product_models:
                    standard_product_model = product_model
                    break
                standard_product_model.stock_type = 1
                standard_product_model.stocks = standard_model_property.get('product_store', 0)
                standard_product_model.update()
            else:
                for model_property in model_info:

                    name = model_property.get('name')
                    product_model = ProductModel.from_product_id_name({'product_id': product_id,
                                                                       'name': name})
                    product_model.stock_type = 1
                    product_model.stocks = model_property.get('stocks', 0)
                    product_model.update()
            return {
                'SUCCESS': True
            }
        except:
            msg = unicode_full_stack()
            watchdog.info(msg)
            return {
                'SUCCESS': False
            }
