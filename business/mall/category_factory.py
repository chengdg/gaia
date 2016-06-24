# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.category import Category, CategoryHasProduct
from business.mall.product import Product

class CategoryFactory(business_model.Model):
    '''
    分组创建工厂@生成器
    '''
    __slots__=(
        )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    def create():
        category_factory_obj = CategoryFactory()
        return category_factory_obj

    def save(self, owner_id, name):
        category = Category.empty_category()
        category_model =category.save(owner_id, name)
        return category_model

class CategoryHasProductFactory(business_model.Model):
    '''
    创建分组中商品关系@生成器
    '''
    __slots__=(
        )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    def create():
        category_has_product_obj = CategoryHasProductFactory()
        return category_has_product_obj

    def save(self, product_ids, category_obj):
        category_has_product_objs = []
        category_has_product_obj = CategoryHasProduct.empty_cateogry_has_product()
        for product_id in product_ids:
            product_obj = Product.from_id({'product_id': product_id})
            product = product_obj
            category_has_product = category_has_product_obj.save(category_obj, product)
            category_has_product_objs.append(category_has_product)
        return category_has_product_objs


