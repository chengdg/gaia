# -*- coding: utf-8 -*-
__author__ = "charles"

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.factory.product_property_factory import ProductPropertyFactory, ProductTemplatePropertyFactory
from business.mall.product_property import ProductPropertyTemplate, ProductTemplateProperty


class AProductPropertyTemplate(api_resource.ApiResource):
    """
    商品属性模板管理
    """

    app = 'mall'
    resource = 'product_property_template'

    @param_required(['owner_id', 'title'])
    def put(self):
        """
        添加属性模板
        owner_id 用户id
        title 模板名称
        """
        owner_id = self['owner_id']
        title = self['title']

        # properties = json.loads(self['properties'])

        factory = ProductPropertyFactory.create()
        template = factory.save({
            'owner_id': owner_id,
            'title': title,
            # 'properties': properties
        })
        result = template.to_dict()
        properties = [pro.to_dict() for pro in template.properties]
        result.update({"properties": properties})
        return result

    @param_required(['id'])
    def get(self):
        """
        根据id，获取单个属性模板
        """
        template = ProductPropertyTemplate.from_id(dict(id=self['id']))

        return {
            'template': template.to_dict(),
            'properties': template.properties
        }

    @param_required(['id', 'title'])
    def post(self):
        """
        更新
        id: 属性模板id
        title: 属性模板标题
        """
        title = self['title']
        template_id = self['id']
        try:
            template = ProductPropertyTemplate(None)
            template.id = template_id
            template.name = title
            change_rows = template.update()
            return {"change_rows": change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}

    @param_required(['id'])
    def delete(self):
        """
        删除单个模板
        """
        template_id = self['id']
        try:
            change_rows = ProductPropertyTemplate.delete_from_id({"id": template_id})
            return {"change_rows": change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}


class APropertyTemplateList(api_resource.ApiResource):
    """
    商品属性模板列表
    """
    app = 'mall'
    resource = 'template_list'

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


class AProductTemplateProperty(api_resource.ApiResource):
    """
    商品模板的属性
    """
    app = 'mall'
    resource = 'template_property'

    @param_required(['template_id'])
    def get(self):
        """
        根据模板id获取所有的该模板的所有属性
        """
        template_id = self['template_id']
        properties = ProductTemplateProperty.from_template_id({"template_id": template_id})
        result = [pro.to_dict() for pro in properties]
        return {
            'properties': result
        }

    @param_required(['template_id', 'properties', 'owner_id'])
    def put(self):
        """
        创建模板的属性(多个属性）
        properties: [{name:name, value:value}]
        """
        template_id = self['template_id']
        properties = self['properties']
        owner_id = self['owner_id']
        properties = json.loads(properties)
        factory = ProductTemplatePropertyFactory.create()
        if len(properties) == 1:

            # @param_required(['template_id', 'name', 'value', 'owner_id'])
            try:
                rs = factory.save({'template_id': template_id,
                                   'name': properties[0]['name'],
                                   'value': properties[0]['value'],
                                   'owner_id': owner_id
                                   })
                return rs.to_dict()
            except:
                msg = unicode_full_stack()
                watchdog.error(msg)
                return None
        else:
            # @param_required(['template_id', 'properties', 'owner_id'])
            try:
                rs = factory.save_many({
                    'template_id': template_id,
                    'owner_id': owner_id,
                    'properties': properties
                })
                results = [pro.to_dict() for pro in rs]

                return {
                    "results": results
                }
            except:
                msg = unicode_full_stack()
                watchdog.error(msg)
                return None

    @param_required(['properties'])
    def post(self):
        """
        更新
        """
        properties = self['properties']
        properties = json.loads(properties)
        change_rows = 0
        try:
            for pro in properties:
                template_property = ProductTemplateProperty(None)
                template_property.id = pro['id']
                template_property.name = pro['name']
                template_property.value = pro['value']
                template_property.update()
                change_rows += 1
            return {
                "change_rows": change_rows
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}

    @param_required(['ids'])
    def delete(self):
        """

        """

        ids = self['ids']
        ids = json.loads(ids)
        try:

            change_rows = ProductTemplateProperty.delete_from_ids({"ids": ids})
            return {"change_rows": change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}