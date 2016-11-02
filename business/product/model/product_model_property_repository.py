# -*- coding: utf-8 -*-
__author__ = 'charles'

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from business.product.model.product_model_property import ProductModelProperty
from business.product.model.product_model_property_value import ProductModelPropertyValue


class ProductModelPropertyRepository(business_model.Service):
    """
    商品规格属性的repository
    """
    def get_properties(self):
        """
        获得corp的商品属性规格集合
        """
        property_models = mall_models.ProductModelProperty.select().dj_where(owner_id=self.corp.id, is_deleted=False)

        datas = []
        for property_model in property_models:
            datas.append(ProductModelProperty.from_model(property_model))

        return datas

    def get_property(self, property_id):
        """
        获得corp中指定的商品属性规格
        """
        property_model = mall_models.ProductModelProperty.select().dj_where(owner_id=self.corp.id, id=property_id).get()
        return ProductModelProperty.from_model(property_model)

    def get_property_value(self, property_value_id):
        property_value_model = mall_models.ProductModelPropertyValue.select().dj_where(id=property_value_id).get()
        return ProductModelPropertyValue(property_value_model)

    def delete_property(self, property_id):
        """
        删除指定的商品规格属性
        """
        mall_models.ProductModelProperty.update(is_deleted=True).dj_where(owner_id=self.corp.id, id=property_id).execute()

    def delete_property_value(self, property_value_id):
        """
        删除指定的商品规格属性的属性值
        """
        mall_models.ProductModelPropertyValue.update(is_deleted=True).dj_where(id=property_value_id).execute()
