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

    @param_required(['model_property_id', 'name'])
    def put(args):
        """
        添加
        model_property_id -- 规格id
        name -- 规格值的名字
        pic_url -- 规格值的图片地址(非必须)
        """
        model_property_id = args['model_property_id']
        name = args['name']
        pic_url = args.get('pic_url', '')

        try:
            model_property_value = ProductModelPropertyValue.create({
                                        "property_id": model_property_id,
                                        "name": name,
                                        "pic_url": pic_url})
            return model_property_value
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {
                'product_model_value': None
            }

    @param_required(['id'])
    def delete(self):
        """
        id -- 规格属性id
        """
        model_property = ProductModelPropertyValue(None)
        try:
            model_property.delete_from_id({'id': self['id']})
            return {"msg": "Delete success"}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "Delete failed"}