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

    @param_required(['corp'])
    def get(args):
        """
        规格列表
        """
        corp = args['corp']
        model_properties = corp.product_model_property_repository.get_properties()

        datas = []
        for model_property in model_properties:
            datas.append({
                "id": model_property.id,
                "name": model_property.name,
                "type": model_property.type,
                "values": []
            })

        return {
            "product_model_properties": datas
        }