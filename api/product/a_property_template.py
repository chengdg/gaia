# -*- coding: utf-8 -*-
__author__ = "charles"

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_property import ProductPropertyTemplate, ProductTemplateProperty


class AProductTemplateProperty(api_resource.ApiResource):
    """
    商品模板的属性
    """
    app = 'product'
    resource = 'property_template'

    @param_required(['template_id', 'owner_id'])
    def get(args):
        """
        获得模板信息:包括模板本身信息和其中属性信息
        """
        template_id = args['template_id']
        properties = ProductTemplateProperty.from_template_id({"template_id": template_id})
        temmplate = ProductPropertyTemplate.from_id({'id': template_id})
        properties = [pro.to_dict() for pro in properties]
        return {
            'template': temmplate.to_dict(),
            'properties': properties
        }

    @param_required(['template_id'])
    def delete(args):
        """
        删除单个模板
        """
        template_id = args['id']
        try:
            change_rows = ProductPropertyTemplate.delete_from_id({"id": template_id})
            return {"change_rows": change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}

    @param_required(['owner_id','title', 'newProperties'])
    def put(args):
        """创建属性模板

        Args:
          title: 属性模板标题
          newProperties 属性模板中需要新建的property信息的json字符串

        Example:
          {
            'title': 'aaa',
            'newProperties':[
                {
                    id: -1, //id=-1, 代表需要新建的属性
                    name: "属性1",
                    value: "属性1的描述"
                },
                ...
            ]
          }
        """

        new_properties = json.loads(args.get('newProperties', "[]"))
        ProductPropertyTemplate.create({'owner_id': args['owner_id'], 'title': args['title'], 'new_properties': new_properties})

        return {}

    @param_required(['owner_id', 'template_id','title', 'newProperties','updateProperties','deletedIds'])
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
        new_properties = json.loads(args.get('newProperties', "[]"))
        update_properties = json.loads(args.get('updateProperties', "[]"))
        deleted_property_ids = json.loads(args.get('deletedIds', "[]"))

        ProductPropertyTemplate.modify({
            'template_id': template_id,
            'title': title,
            'new_properties': new_properties,
            'update_properties': update_properties,
            'deleted_property_ids': deleted_property_ids

        })

        return {}
