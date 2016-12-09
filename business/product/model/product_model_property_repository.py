# -*- coding: utf-8 -*-
__author__ = 'charles'
from bdem import msgutil
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from business.product.model.product_model_property import ProductModelProperty
from business.product.model.product_model_property_value import ProductModelPropertyValue
from gaia_conf import TOPIC


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

    def get_order_product_model_values(self, product_model_names):
        """
        获取订单商品的model详情
        """
        product_model_name2value = {}
        product_model_value_ids = []
        for product_model_name in product_model_names:
            if product_model_name != 'standard':
                product_model_value_ids += [detail.split(':')[1] for detail in product_model_name.split('_')]
        property_value_models = mall_models.ProductModelPropertyValue.select().dj_where(id__in=list(set(product_model_value_ids)))
        id2property_value_model = dict([(model.id, model) for model in property_value_models])

        for product_model_name in product_model_names:
            if product_model_name == 'standard':
                product_model_name2value[product_model_name] = []
            else:
                property_value_ids = [detail.split(':')[1] for detail in product_model_name.split('_')]
                data = []
                for value_id in property_value_ids:
                    property_value_model = id2property_value_model[int(value_id)]
                    data.append(ProductModelPropertyValue(property_value_model))
                product_model_name2value[product_model_name] = data
        return product_model_name2value

    def delete_property(self, property_id):
        """
        删除指定的商品规格属性
        """
        mall_models.ProductModelProperty.update(is_deleted=True).dj_where(owner_id=self.corp.id, id=property_id).execute()
        # 发送更新缓存的消息
        msgutil.send_message(
            TOPIC['product'],
            'product_model_property_deleted',
            {'corp_id': self.corp.id, 'product_model_property_id': property_id}
        )

    def delete_property_value(self, property_value_id):
        """
        删除指定的商品规格属性的属性值
        """
        mall_models.ProductModelPropertyValue.update(is_deleted=True).dj_where(id=property_value_id).execute()
        # 发送更新缓存的消息
        msgutil.send_message(
            TOPIC['product'],
            'product_model_property_value_deleted',
            {'corp_id': self.corp.id, 'product_model_property_value': property_value_id}
        )