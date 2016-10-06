# -*- coding: utf-8 -*-
__author__ = 'Eugene'

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

class AProductModelProperties(api_resource.ApiResource):
    """
    商品规格列表
    """
    app = 'product'
    resource = 'model_properties'

    @param_required(['corp_id'])
    def get(args):
        """
        规格列表
        """
        corp = args['corp']
        model_properties = corp.product_model_property_repository.get_properties()

        datas = []
        for model_property in model_properties:
            data = {
                "id": model_property.id,
                "name": model_property.name,
                "type": model_property.type,
                "values": []
            }

            for property_value in model_property.values:
                data['values'].append({
                    "id": property_value.id,
                    "name": property_value.name,
                    "pic_url": property_value.pic_url
                })

            datas.append(data)

        return {
            "product_model_properties": datas
        }