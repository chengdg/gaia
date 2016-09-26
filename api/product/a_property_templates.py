# -*- coding: utf-8 -*-
__author__ = "charles"

from eaglet.core import api_resource
from eaglet.decorator import param_required

class APropertyTemplates(api_resource.ApiResource):
    """
    商品属性模板列表
    """
    app = 'product'
    resource = 'property_templates'

    @param_required(['corp'])
    def get(args):
        """
        根据用户id，获取所有的属性模板
        """
        corp = args['corp']
        templates = corp.product_property_template_repository.get_templates()

        datas = []
        for template in templates:
            data = {
                "id": template.id,
                "name": template.name,
                "properties": []
            }

            for template_property in template.properties:
                data['properties'].append({
                    "id": template_property.id,
                    "name": template_property.name,
                    "value": template_property.value
                })

            datas.append(data)

        return {
            "templates": datas
        }