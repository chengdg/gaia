# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.product import Product

class AProductCategory(business_model.Model):
    '''
    产品分组
    '''
    def __init__(self, model):
        business_model.Model.__init__(self) 


    @staticmethod
    @param_required(['name', 'owner', 'product_ids'])
    def  post_for_category(args):
        '''
        创建商品分组
        '''
        opt = dict(
            owner=args['owner'],
            name=args['name'],
            product_count=len(args['product_ids'])
        )
        obj, created = mall_models.ProductCategory.get_or_create(**opt)
        # created is True or False  
        # If an object is found, get_or_create() returns a tuple of that object and False. 
        # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
        # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
        categoryhasproduct = obj.to_dict()
        if args['product_ids']:
            products = ACategoryHasProductRelation.post_for_category_has_product(dict(product_ids=args['product_ids'], category_obj=obj))
            categoryhasproduct.update(products)
        return categoryhasproduct


class ACategoryHasProductRelation(business_model.Model):
    '''
    建立分组，商品关系
    '''
    def __init__(self, model):
        business_model.Model.__init__(self) 

    @staticmethod
    @param_required(['product_ids', 'category_obj'])
    def post_for_category_has_product(args):
        '''
        创建分组中商品关系对象
        #  还可以优化,使用批处理
        '''
        products = list()
        for product_id in args['product_ids']:
            opt =dict(
                product=mall_models.Product.get(id=product_id),
                category=args['category_obj']
            )
            obj, created = mall_models.CategoryHasProduct.get_or_create(**opt)
            products.append(obj.to_dict())
        return {
            'products': products
        }
