# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models


from business.mall.product import Product

class Categories(business_model.Model):
    """
    商品分组
    """
    __slots__ = (
        'id',
        'owner_id',
        'name',
        'pric_url',
        'product_count',
        'display_index',
        'created_at',
        'products'
    )
    def __init__(self, model, product_ids=[]):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            if product_ids:
                model.products = CategoryHasProduct.post_category_has_product({'product_ids': product_ids, 'category_obj': model})
            else:
                model.products = CategoryHasProduct.get_category_has_product({'db_model': model})
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['owner'])
    def  get_for_category(args):
        '''
        分组管理列表
        '''
        filter_params = {'owner': args['owner'] }
        if args['category_ids']:
            filter_params.update({'id__in': args['category_ids']})
        categories = mall_models.ProductCategory.filter(**filter_params) 
        return [Categories(category) for category in categories]

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
        return Categories(obj, product_ids=args['product_ids'])


class CategoryHasProduct(business_model.Model):
    '''
    分组领域中商品值对象
    '''
    __slots__ = (
        'products'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def get_category_has_product(args):
        model = args['db_model']
        relations = mall_models.CategoryHasProduct.filter(category=model)
        product_ids = [relation.product_id for relation in relations]
        return Product.from_ids({'product_ids': product_ids})

    @staticmethod
    @param_required(['product_ids', 'category_obj'])
    def post_category_has_product(args):
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
            products.append(Product(mall_models.Product(obj)))
        return products
