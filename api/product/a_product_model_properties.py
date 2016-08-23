# -*- coding: utf-8 -*-
__author__ = 'Eugene'

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business.product.product_model_property import ProductModelProperty

class AProductModelProperties(api_resource.ApiResource):
    """
    商品规格列表
    """
    app = 'product'
    resource = 'model_properties'

    @param_required(['owner_id'])
    def get(args):
        """
        规格列表
        """
        try:
            owner_id = args['owner_id']
            result = ProductModelProperty.from_owner_id({"owner_id": owner_id})
            return {
                'product_model_properties': result
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "Get product model property list failed"}