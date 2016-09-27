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
        'type',
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

        if self.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT:
            self.type = 'text'
        else:
            self.type = 'image'

    @staticmethod
    def from_model(db_model):
        product_model_property = ProductModelProperty(db_model)
        return product_model_property

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

    def update(self, field, value):
        """
        更新
        """
        if field == 'name':
            #更新name
            mall_models.ProductModelProperty.update(name=value).dj_where(id=self.id).execute()
        elif field == 'type':
            #更新type
            model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
            if self.type == 'image':
                model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
            mall_models.ProductModelProperty.update(type=model_type).dj_where(id=self.id).execute()

    @staticmethod
    @param_required(['corp', 'name', 'type'])
    def create(args):
        #确定type
        type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        if args['type'] == 'image':
            type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE

        product_model = mall_models.ProductModelProperty.create(
                            name=args['name'],
                            type=type,
                            owner=args['corp'].id
                        )

        if product_model:
            model = ProductModelProperty(product_model)
            return model
        else:
            return None
