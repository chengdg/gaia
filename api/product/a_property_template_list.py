# -*- coding: utf-8 -*-
__author__ = "charles"

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.factory.product_property_factory import ProductPropertyFactory, ProductTemplatePropertyFactory
from business.mall.product_property import ProductPropertyTemplate, ProductTemplateProperty


class APropertyTemplateList(api_resource.ApiResource):
    """
    商品属性模板列表
    """
    app = 'product'
    resource = 'property_template_list'

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