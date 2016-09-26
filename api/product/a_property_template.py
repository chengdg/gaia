# -*- coding: utf-8 -*-
__author__ = "charles"

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.product.product_property_template import ProductPropertyTemplate


class AProductPropertyTemplate(api_resource.ApiResource):
    """
    商品模板
    """
    app = 'product'
    resource = 'property_template'

    @param_required(['corp', 'template_id'])
    def get(args):
        corp = args['corp']
        template_id = args['template_id']
        template = corp.product_property_template_repository.get_template(template_id)

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
        return {
            'template': data
        }

    @param_required(['corp', 'id'])
    def delete(args):
        corp = args['corp']
        template_id = args['id']
        template = corp.product_property_template_repository.delete_template(template_id)

        return {}

    @param_required(['title', 'new_properties'])
    def put(args):
        """创建属性模板

        Args:
          title: 属性模板标题
          new_properties 属性模板中需要新建的property信息的json字符串

        Example:
          {
            'title': 'aaa',
            'new_properties':[
                {
                    id: -1, //id=-1, 代表需要新建的属性
                    name: "属性1",
                    value: "属性1的描述"
                },
                ...
            ]
          }
        """
        corp = args['corp']
        title = args['title']
        new_properties = args.get('new_properties', "[]")
        try:
            new_properties = json.loads(new_properties)
            ProductPropertyTemplate.create({
                'corp': corp, 
                'title': title, 
                'new_properties': new_properties
            })
            
            return {}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "create template failed"}

    @param_required(['id', 'title', 'new_properties', 'update_properties', 'deleted_ids'])
    def post(args):

        """更新属性模板

        Args:
          id: 属性模板id
          title: 属性模板标题
          newProperties: 属性模板中需要新建的property信息的json字符串
          updateProperties: 属性模板中需要更新的property信息的json字符串
          deletedIds: 属性模板中需要删除的property的id数据的json字符串

        """
        template_id = args['id']
        title = args['title']
        new_properties = json.loads(args.get('new_properties', "[]"))
        update_properties = json.loads(args.get('update_properties', "[]"))
        deleted_property_ids = json.loads(args.get('deleted_ids', "[]"))

        corp = args['corp']
        corp.product_property_template_repository.get_template(template_id).update({
            'title': title,
            'new_properties': new_properties,
            'update_properties': update_properties,
            'deleted_property_ids': deleted_property_ids
        })
        
        return {}
