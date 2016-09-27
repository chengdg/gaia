# -*- coding: utf-8 -*-
__author__ = 'Eugene'

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.product.product_model_property_value import ProductModelPropertyValue

class AProductModelPropertyValue(api_resource.ApiResource):
    """
    商品规格的属性
    """
    app = 'product'
    resource = 'model_property_value'

    @param_required(['model_property_id'])
    def put(args):
        """
        """
        corp = args['corp']
        property_id = args['model_property_id']
        model_property = corp.product_model_property_repository.get_property(property_id)

        name = args.get('name', '')
        pic_url = args.get('pic_url', '')
        property_value = model_property.add_property_value(name, pic_url)

        return {
            "id": property_value.id
        }

    @param_required(['id'])
    def delete(args):
        """
        id -- 规格属性值的id
        """
        corp = args['corp']
        property_value_id = args['id']
        corp.product_model_property_repository.delete_property_value(property_value_id)
        
        return {}