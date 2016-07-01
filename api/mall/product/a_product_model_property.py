# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

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

    @param_required(['owner_id', 'type'])
    def put(self):
        """
        添加规格
        owner_id -- 用户id
        type -- 规格类型　可以为空，但是必须传递，默认是text(text)类型,image:图片类型
        name -- 规格名　
        """
        owner_id = self['owner_id']
        model_type = self['type']
        name = self.get('name', "")

        factory = ProductModelPropertyFactory.create()
        try:
            product_model = factory.save({"owner_id": owner_id,
                                          "type": model_type,
                                          "name": name})
            return {"product_model": product_model.to_dict()}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                "product_model": None
            }

    @param_required(['type', 'id'])
    def post(self):
        """
        更新规格
        id -- 规格ｉｄ
        type -- 规格类型　可以为空，但是必须传递，默认是text(text)类型,image:图片类型
        name -- 规格名　
        """

        model_type = self['type']
        name = self.get('name', '')
        model_id = self['id']

        resource_model = ProductModelProperty(None)
        resource_model.type = model_type
        resource_model.name = name
        resource_model.id = model_id
        try:
            change_rows = resource_model.update()
            return {
                'change_rows': change_rows
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                'change_rows': -1
            }

    @param_required(['id'])
    def get(self):
        """
        获取单个规格
        """
        model_id = self['id']
        product_model = ProductModelProperty.from_id({'id': model_id})
        return {
            "product_model": product_model.to_dict(),
            'properties': product_model.properties
        }

    @param_required(['id'])
    def delete(self):
        try:
            change_rows = ProductModelProperty.delete_from_id({"id": self['id']})
            return {'change_rows': change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {'change_rows': -1}


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
            'product_models': result
        }


class AProductModelPropertyValue(api_resource.ApiResource):
    """
    商品规格的属性
    """
    app = 'mall'
    resource = 'model_property_value'

    @param_required(['id', 'name'])
    def put(self):
        """
        添加
        id -- 规格id
        name -- 规格值的名字
        pic_url -- 规格值的图片地址(非必须)
        """
        model_id = self['id']
        name = self['name']
        pic_url = self.get('pic_url', '')

        factory = ProductModelPropertyValueFactory.create()
        try:
            model_property = factory.save({"model_id": model_id,
                                           "name": name,
                                           "pic_url": pic_url})
            return {
                'product_model_value': model_property.to_dict()
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                'product_model_value': None
            }

    @param_required(['id', 'name'])
    def post(self):
        """
        更新
        id -- 属性值id
        name -- 规格值的名字
        pic_url -- 规格值的图片地址(非必须)
        """
        model_id = self['id']
        name = self['name']
        pic_url = self.get('pic_url', '')

        resource_model = ProductModelPropertyValue(None)
        resource_model.id = model_id
        resource_model.name = name
        resource_model.pic_url = pic_url
        try:
            change_rows = resource_model.update()
            return {"change_rows": change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}

    @param_required(['id'])
    def get(self):
        """
        id -- 规格属性id
        """
        product_model = ProductModelPropertyValue.from_id({'id': self['id']})
        return {
            'product_model_value': product_model.to_dict()
        }

    @param_required(['id'])
    def delete(self):
        """
        id -- 规格属性id
        """
        model_property = ProductModelPropertyValue(None)
        try:
            change_rows = model_property.delete_from_id({'id': self['id']})
            return {"change_rows": change_rows}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {"change_rows": -1}
