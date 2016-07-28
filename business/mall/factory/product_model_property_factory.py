# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from business.mall.product_model_property import ProductModelPropertyValue, ProductModelProperty
from business.account.user_profile import UserProfile


class ProductModelPropertyFactory(business_model.Model):
    """
    商品属性规格工厂类
    """
    def __init__(self):
        super(ProductModelPropertyFactory, self).__init__()

    @staticmethod
    def create():
        return ProductModelPropertyFactory()

    @staticmethod
    @param_required(['owner_id', 'type', 'name'])
    def save(args):
        """
        创造新规格
        """
        owner_id = args['owner_id']
        try:
            owner_id = int(owner_id)
        except:
            # 获取mall_type = 2的平台
            user_profiles = UserProfile.from_webapp_type({'webapp_type': 2})
            if user_profiles:
                owner_id = user_profiles[0].user_id
            else:
                return None
        model_property = ProductModelProperty(None)
        model_property.owner_id = owner_id
        model_property.type = args['type']
        model_property.name = args['name']
        rs_model = model_property.save()
        return rs_model


class ProductModelPropertyValueFactory(business_model.Model):
    """

    """

    def __init__(self):
        super(ProductModelPropertyValueFactory, self).__init__()

    @staticmethod
    def create():
        """
        创建
        """
        return ProductModelPropertyValueFactory()

    @staticmethod
    @param_required(["model_id", 'name', 'pic_url'])
    def save(args):
        model_property_value = ProductModelPropertyValue(None)
        model_property_value.name = args['name']
        model_property_value.pic_url = args['pic_url']
        rs = model_property_value.save(model_id=args['model_id'])
        return rs
