# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.categories import Categories

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
        category = Categories.save({'owner_id': owner_id, 'name': name})
        return category

class CategoryHasProductFactory(business_model.Model):
    '''
    创建分组中商品关系@生成器
    '''
    __slots__=(
        )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    def create(self):
        category_has_product_obj = CategoryHasProductFactory()
        return category_has_product_obj

    @param_required(['product_ids', 'category_id'])
    def save(self, product_ids, category_id):
        category_obj = mall_models.ProductCategory.get(id=category_id)
        category_has_product_objs = []
        for product_id in product_ids:
            opt = {
                'product': mall_models.Product.get(id=product_id),
                'category': category_obj
            }
           # created is True or False  
            # If an object is found, get_or_create() returns a tuple of that object and False. 
            # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
            # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
            obj, created = mall_models.CategoryHasProduct.get_or_create(**opt)
            category_has_product_objs.append(obj)
        return category_has_product_objs


