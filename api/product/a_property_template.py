# -*- coding: utf-8 -*-
__author__ = "charles"

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.product.product_property import ProductPropertyTemplate, ProductTemplateProperty


class AProductTemplateProperty(api_resource.ApiResource):
    """
    商品模板的属性
    """
    app = 'product'
    resource = 'property_template'

    @param_required(['template_id'])
    def get(args):
        """
        获得模板信息:包括模板本身信息和其中属性信息
        """
        try:
            template_id = args['template_id']
            properties = ProductTemplateProperty.from_template_id({"template_id": template_id})
            temmplate = ProductPropertyTemplate.from_id({'id': template_id})
            properties = [pro.to_dict() for pro in properties]
            temmplate = temmplate.to_dict()
            temmplate['properties'] = properties
            return {
                'template': temmplate
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "get id=%s template failed" % template_id}

    @param_required(['template_id'])
    def delete(args):
        """
        删除单个模板
        """
        template_id = args['template_id']
        try:
            change_rows = ProductPropertyTemplate.delete_from_id({"id": template_id})
            return {"msg": "delete success"}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "delete failed"}

    @param_required(['owner_id','title', 'new_properties'])
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

        owner_id = args['owner_id']
        title = args['title']
        new_properties = args.get('new_properties', "[]")
        try:
            new_properties = json.loads(new_properties)
            ProductPropertyTemplate.create({'owner_id': owner_id, 'title': title, 'new_properties': new_properties})
            return {}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "create template failed"}

    @param_required(['owner_id', 'template_id','title', 'new_properties','update_properties','deleted_ids'])
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
        try:
            ProductPropertyTemplate.modify({
                'template_id': template_id,
                'title': title,
                'new_properties': new_properties,
                'update_properties': update_properties,
                'deleted_property_ids': deleted_property_ids

            })
            return {}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {"msg": "update template failed"}
