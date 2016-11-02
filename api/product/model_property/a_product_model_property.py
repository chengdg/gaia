# -*- coding: utf-8 -*-
__author__ = 'charles'

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.decorator import param_required

from business.product.model.product_model_property import ProductModelProperty


class AProductModelProperty(api_resource.ApiResource):
    """
    商品规格属性
    """
    app = 'product'
    resource = 'model_property'

    @staticmethod
    def __format_product_model_property(model_property):
        data = {
            "id": model_property.id,
            "name": model_property.name,
            "type": model_property.type,
            "values": []
        }

        for property_value in model_property.values:
            data['values'].append({
                "id": property_value.id,
                "name": property_value.name,
                "pic_url": property_value.pic_url
            })

        return data

    @param_required(['corp_id', 'id'])
    def get(args):
        """
        获取单个规格
        """
        corp = args['corp']
        property_id = args['id']
        model_property = corp.product_model_property_repository.get_property(property_id)

        data = AProductModelProperty.__format_product_model_property(model_property)
        return {
            "product_model_property": data
        }

    @param_required(['corp_id', 'type'])
    def put(args):
        """
        添加规格属性
        corp_id -- corp_id
        type -- 规格属性类型　可以为空，但是必须传递，默认是text(text)类型, image:图片类型
        name -- 规格属性名
        """
        corp = args['corp']
        type = args['type']
        name = args.get('name', "")

        model_property = ProductModelProperty.create({
            "corp": corp,
            "name": name,
            "type": type
        })

        data = AProductModelProperty.__format_product_model_property(model_property)
        return {
            "product_model_property": data
        }

    @param_required(['corp_id', 'id', 'field', 'value'])
    def post(args):
        """
        更新规格属性
        """
        corp = args['corp']
        property_id = args['id']
        product_model_property = corp.product_model_property_repository.get_property(property_id)

        field = args['field']
        value = args['value']
        product_model_property.update(field, value)

        return {}

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        property_id = args['id']
        corp.product_model_property_repository.delete_property(property_id)

        return {}
