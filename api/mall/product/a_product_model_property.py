# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_model_property import ProductModelProperty
from business.mall.product_model_property import ProductModelPropertyValue
from business.mall.factory.product_model_property_factory import ProductModelPropertyFactory, \
    ProductModelPropertyValueFactory


class AProductModelProperty(api_resource.ApiResource):
    """
    商品规格属性
    """

    app = 'mall'
    resource = 'product_model_property'

    @param_required(['owner_id', 'type', 'name'])
    def put(self):
        """
        添加规格
        owner_id -- 用户id
        type -- 规格类型　可以为空，但是必须传递，默认是0(text)类型,1:图片类型
        name -- 规格名　可以为空，但是必须传递
        """
        owner_id = self['owner_id']
        model_type = self['type']
        name = self['name']

        resource_model = ProductModelProperty(None)
        resource_model.owner_id = owner_id
        resource_model.type = model_type
        resource_model.name = name

        result, msg = ProductModelPropertyFactory.create(resource_model)
        return {
            'result': result,
            'msg': msg
        }

    @param_required(['type', 'name', 'id'])
    def post(self):
        """
        更新规格
        id -- 规格ｉｄ
        type -- 规格类型　可以为空，但是必须传递，默认是0(text)类型,1:图片类型
        name -- 规格名　可以为空，但是必须传递
        """

        model_type = self['type']
        name = self['name']
        model_id = self['id']

        resource_model = ProductModelProperty(None)
        resource_model.type = model_type
        resource_model.name = name
        resource_model.id = model_id

        result, msg = ProductModelPropertyFactory.save({"resource_model": resource_model})
        return {
            'result': result,
            'msg': msg
        }

    @param_required(['id'])
    def get(self):
        """
        获取单个规格
        """
        model_id = self['id']
        entry = ProductModelProperty.from_id(dict(id=model_id))
        return {
            "entry": entry,
            'properties': entry.properties
        }

    @param_required(['id'])
    def delete(self):
        result, msg = ProductModelPropertyFactory.delete_from_id(dict(id=self['id']))
        return {
            'result': result,
            'msg': msg
        }


class AProductModelPropertyList(api_resource.ApiResource):
    """
    商品规格列表
    """
    app = 'mall'
    resource = 'product_model_property_list'

    @param_required(['owner_id'])
    def get(self):
        """
        规格列表
        """
        result = ProductModelProperty.from_owner_id({"owner_id": self['owner_id']})
        return {
            'entries': result
        }


class AProductModelPropertyValue(api_resource.ApiResource):
    """
    商品规格的属性
    """
    app = 'mall'
    resource = 'model_property_value'

    @param_required(['id', 'name', 'pic_url'])
    def put(self):
        """
        添加
        id -- 规格id
        name -- 规格值的名字
        pic_url -- 规格值的图片地址()
        """
        model_id = self['id']
        name = self['name']
        pic_url = self['pic_url']

        resource_model = ProductModelPropertyValue(None)
        resource_model.id = model_id
        resource_model.name = name
        resource_model.pic_url = pic_url

        result, msg = ProductModelPropertyValueFactory.create(resource_model)
        return {
            'result': result,
            'msg': msg
        }

    @param_required(['id', 'name', 'pic_url'])
    def post(self):
        """
        更新
        id -- 属性值id
        name -- 规格值的名字
        pic_url -- 规格值的图片地址()
        """
        model_id = self['id']
        name = self['name']
        pic_url = self['pic_url']

        resource_model = ProductModelPropertyValue(None)
        resource_model.id = model_id
        resource_model.name = name
        resource_model.pic_url = pic_url

        result, msg = ProductModelPropertyValueFactory.save(resource_model)
        return {
            'result': result,
            'msg': msg
        }

    @param_required(['id'])
    def get(self):
        """
        id -- 规格属性id
        """
        entry = ProductModelPropertyValue.from_id({'id': self['id']})
        return {
            'entry': entry
        }

    @param_required(['id'])
    def delete(self):
        """
        id -- 规格属性id
        """
        result, msg = ProductModelPropertyValueFactory.delete_from_id({'id': self['id']})
        return {
            'result': result,
            'msg': msg
        }
