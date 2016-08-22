# -*- coding: utf-8 -*-
__author__ = "charles"

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_property import ProductPropertyTemplate


class APropertyTemplates(api_resource.ApiResource):
    """
    商品属性模板列表
    """
    app = 'product'
    resource = 'property_templates'

    @param_required(['owner_id'])
    def get(self):
        """
        根据用户id，获取所有的属性模板
        """
        templates = ProductPropertyTemplate.from_owner_id({'owner_id': self['owner_id']})
        result = []

        for template in templates:
            temp = template.to_dict()
            properties = [pro.to_dict() for pro in template.properties]
            temp.update({"properties": properties})
            result.append(temp)
        return {
            "templates": result
        }