# -*- coding: utf-8 -*-
__author__ = 'charles'

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.decorator import param_required

from business.product.product_model_property import ProductModelProperty


class AProductModelProperty(api_resource.ApiResource):
    """
    商品规格属性
    """

    app = 'product'
    resource = 'model_property'

    @param_required(['owner_id', 'type'])
    def put(args):
        """
        添加规格
        owner_id -- 用户id
        type -- 规格类型　可以为空，但是必须传递，默认是text(text)类型,image:图片类型
        name -- 规格名　
        """
        owner_id = args['owner_id']
        type = args['type']
        name = args.get('name', "")

        try:
            product_model_property = ProductModelProperty.create({
                                "owner_id": owner_id,
                                "type": type,
                                "name": name})
            return {"product_model_property": product_model_property.to_dict()}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {
                "msg": "Create failed"
            }

    @param_required(['type', 'id', 'name'])
    def post(args):
        """
        更新规格
        id -- 规格ｉｄ
        type -- 规格类型　可以为空，但是必须传递，默认是text(text)类型,image:图片类型
        name -- 规格名　
        """

        model_id = args['id']
        model_type = args['type']
        name = args['name']

        resource_model = ProductModelProperty(None)
        resource_model.type = model_type
        resource_model.name = name
        resource_model.id = model_id
        try:
            change_rows = resource_model.update()
            if change_rows:
                return {"msg": "Update success"}
            else:
                return 500, {"msg": "model(id:%s) not found or have deleted" % model_id}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {
                "msg": "Update failed"
            }

    @param_required(['id'])
    def get(args):
        """
        获取单个规格
        """
        model_id = args['id']
        product_model_property = ProductModelProperty.from_id({'id': model_id})
        return {
            "product_model_property": product_model_property.to_dict(),
            'properties': product_model_property.properties
        }

    @param_required(['id'])
    def delete(args):
        try:
            model_id = args['id']
            ProductModelProperty.delete_from_id({"id": model_id})
            return {'msg': 'Delete success'}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {'msg': 'Delete failed'}