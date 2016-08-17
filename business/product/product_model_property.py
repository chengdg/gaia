# -*- coding: utf-8 -*-
__author__ = 'charles'

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from business.product.product_model_property_value import ProductModelPropertyValue


class ProductModelProperty(business_model.Model):
    """
    商品的规格管理
    """

    __slots__ = (
        'id',
        'name',
        'owner_id',
        'type',
    )

    def __init__(self, model):
        super(ProductModelProperty, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        product_model_property = mall_models.ProductModelProperty.select()\
            .dj_where(id=args['id'], is_deleted=False).first()

        if product_model_property:

            # 使用from_model将数据取回到领域模型
            _model = ProductModelProperty(product_model_property)
            _model.type = 'text' if _model.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image'
            return _model
        return None

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product_model_property = ProductModelProperty(model)
        product_model_property.type = 'text' \
            if product_model_property.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image'
        return product_model_property

    @staticmethod
    @param_required(['owner_id'])
    def from_owner_id(args):
        """
        根据用户id获取所有属性模板
        """
        templates = mall_models.ProductModelProperty.select().dj_where(
                                    owner_id=args['owner_id'],
                                    is_deleted=False
                    )
        result = []
        for template in templates:
            _model = ProductModelProperty(template)
            _model.type = 'text' if _model.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image'
            model_dict = _model.to_dict()
            model_dict['value'] = _model.properties
            result.append(model_dict)
        return result

    @property
    def properties(self):
        """
        """
        properties = self.context.get('properties', None)
        if not properties and self.id:
            return ProductModelPropertyValue.from_model_id({'model_id': self.id})
        return properties

    @properties.setter
    def properties(self, value):
        self.context['properties'] = value

    def update(self):
        """
        更新

        """

        # default 0(text)
        model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        if self.type == 'image':
            model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
        change_rows = mall_models.ProductModelProperty.update(
                                name=self.name,
                                type=model_type,
                                is_deleted=False
                            ).dj_where(id=self.id).execute()
        return change_rows

    @staticmethod
    @param_required(['name', 'type', 'owner_id'])
    def create(args):
        type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        if args['type'] == 'image':
            type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
        product_model = mall_models.ProductModelProperty.create(
                            name=args['name'],
                            type=type,
                            owner=args['owner_id'])
        if product_model:
            model = ProductModelProperty(product_model)
            model.type = 'text' if model.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image'
            return model
        return None

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        mall_models.ProductModelProperty.update(is_deleted=True) \
            .dj_where(id=args.get('id')).execute()
        mall_models.ProductModelPropertyValue.update(is_deleted=True) \
            .dj_where(property=args['id']).execute()
