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
    )
    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['owner_id'])
    def  get_for_category(args):
        '''
        分组管理列表
        '''
        filter_params = {'owner': args['owner_id'] }
        if args['category_ids']:
            filter_params.update({'id__in': args['category_ids']})
        categories = mall_models.ProductCategory.filter(**filter_params) 
        return [Categories(category) for category in categories]

    @staticmethod
    @param_required(['category_id', 'params'])
    def put_category(args):
        mall_models.ProductCategory.update(**args['params']).dj_where(id=args['category_id']).execute()
        return Categories(mall_models.ProductCategory.get(id=args['category_id']))

    @staticmethod
    @param_required(['category_id'])
    def from_id(args):
        '''
        获取单个分组信息
        '''
        obj = mall_models.ProductCategory.select().dj_where(id=args['category_id'])
        if obj.first():
            return Categories(obj.first())
        else:
            return None

    @staticmethod
    @param_required(['owner_id', 'name'])
    def save(args):
        opt = {
            'owner': args['owner_id'],
            'name': args['name']
        }
        # created is True or False  
        # If an object is found, get_or_create() returns a tuple of that object and False. 
        # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
        # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
        # try:
        obj, created = mall_models.ProductCategory.get_or_create(**opt)
        return Categories(obj)

    @staticmethod
    @param_required(['category_id'])
    def delete_from_id(args):
        '''
            删除指定分组
        '''
        obj = mall_models.ProductCategory.get(id=args['category_id'])
        mall_models.CategoryHasProduct.delete().dj_where(category=obj).execute()
        return obj.delete_instance()

    @property
    def products(self):
        category_model = self.context['db_model']
        relations = mall_models.CategoryHasProduct.filter(category=category_model)
        product_ids = [relation.product_id for relation in relations]
        return Product.from_ids({'product_ids': product_ids})


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
    @param_required()
    def get_category_has_product(args):
        pass

