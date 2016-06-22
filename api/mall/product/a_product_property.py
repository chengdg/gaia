# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.factory.product_property_factory import ProductPropertyFactory
from business.mall.product_property import ProductPropertyTemplate


class AProductPropertyTemplate(api_resource.ApiResource):
    """
    商品属性模板管理
    """

    app = 'mall'
    resource = 'product_property_template'

    @param_required(['owner_id', 'title', 'properties'])
    def put(self):
        """
        添加属性模板
        owner_id 用户id
        title 模板名称
        properties 模板属性list[dict(name='', value='')]
        """
        owner_id = self['owner_id']
        title = self['title']
        properties = self['properties']
        if not isinstance(properties, dict):
            properties = json.loads(properties)

        product_property = ProductPropertyTemplate(None)
        # 领域模型对象变量名和model保持一致
        product_property.owner_id = owner_id
        product_property.name = title
        product_property.properties = properties

        result, msg = ProductPropertyFactory.create(product_property)

        return {
            'result': result,
            'msg': msg
        }

    @param_required(['id'])
    def get(self):
        """
        根据id，获取单个属性模板
        """
        template = ProductPropertyTemplate.from_id(dict(id=self['id']))

        return {
            'entry': template,
            'properties': template.properties
        }

    @param_required(['id', 'owner_id', 'newProperties', 'updateProperties', 'deletedIds'])
    def post(self):
        """
        更新
        owner_id: 用户ｉｄ
        id: 属性模板id
        title: 属性模板标题
        newProperties: 属性模板中需要新建的property信息的json字符串[{name:name, value:value}]
        updateProperties: 属性模板中需要更新的property信息的json字符串[{name:name, value:value, id:id}]
        deletedIds: 属性模板中需要删除的property的id数据的json字符串["id"]
        """
        owner_id = self['owner_id']
        template_id = self['id']
        title = self['title']
        new_properties = json.loads(self['newProperties']) if self['newProperties'] else []
        update_properties = json.loads(self['updateProperties']) if self['updateProperties'] else []
        deleted_ids = json.loads(self['deletedIds']) if self['deletedIds'] else []

        result, msg = ProductPropertyFactory.save({'owner_id': owner_id,
                                                   'template_id': template_id,
                                                   'new_properties': new_properties,
                                                   'update_properties': update_properties,
                                                   'deleted_ids': deleted_ids,
                                                   'title': title})
        return {
            'result': result,
            'msg': msg
        }

    @param_required(['id'])
    def delete(self):
        """
        删除单个模板
        """
        template_id = self.get('id')
        result, msg = ProductPropertyFactory.delete_from_id({"id": template_id})
        return {
            "result": result,
            "msg": msg
        }


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
        templates = ProductPropertyTemplate.from_owner_id(dict(owner_id=self['owner_id']))
        return {
            "entries": templates
        }
