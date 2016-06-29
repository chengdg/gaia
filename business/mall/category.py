# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.product import Product


class Category(business_model.Model):
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
    def empty_category(model=None):
         category = Category(model)
         return category

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
        return [Category(category) for category in categories]

    def update_name(self, category_id ,name):
       mall_models.ProductCategory.update(name=name).dj_where(id=category_id).execute()

    def update_product_count(self, category_id, product_count):
        mall_models.ProductCategory.update(product_count=product_count).dj_where(id=category_id).execute()
        
    @staticmethod
    @param_required(['category_id'])
    def from_id(args):
        '''
        获取单个分组信息
        '''
        obj = mall_models.ProductCategory.select().dj_where(id=args['category_id'])
        if obj.first():
            return Category(obj.first())
        else:
            return None

    def save(self, owner_id, name):
        opt = {
            'owner': owner_id,
            'name': name
        }
        # created is True or False  
        # If an object is found, get_or_create() returns a tuple of that object and False. 
        # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
        # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
        # try:
        obj, created = mall_models.ProductCategory.get_or_create(**opt)
        return Category(obj)

    def delete_from_id(self, category_id):
        '''
            删除指定分组
        '''
        obj = mall_models.ProductCategory.get(id=category_id)
        if obj.product_count != 0:
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
    __slots__ =  (
        'id',
        'product_id',
        'category_id',
        'display_index',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def empty_cateogry_has_product(model=None):
        category_has_product_obj = CategoryHasProduct(model)
        return category_has_product_obj

    @staticmethod
    @param_required(['category_has_product_id'])
    def from_id(args):
        category_has_product_obj = mall_models.CategoryHasProduct.select().dj_where(id=args['category_has_product_id'])
        if category_has_product_obj.first():
            return CategoryHasProduct(category_has_product_obj.first())
        else:
            return None

    def save(self, category_obj, product_obj):
            opt = {
                'product': product_obj.context['db_model'],
                'category': category_obj.context['db_model']
            }
           # created is True or False  
            # If an object is found, get_or_create() returns a tuple of that object and False. 
            # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
            # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
            obj, created = mall_models.CategoryHasProduct.get_or_create(**opt)
            return CategoryHasProduct(obj)

    def delete_from_id(self, category_has_product_id):
        category_has_product_obj = mall_models.CategoryHasProduct.get(id=category_has_product_id)
        return category_has_product_obj.delete_instance()

    @staticmethod
    @param_required(['category_id', 'product_id'])
    def  from_category_id_and_product_id(args):
        category_has_product_obj = mall_models.CategoryHasProduct.select().dj_where(category_id=args['category_id'], product_id=args['product_id'])
        if category_has_product_obj.first():
            return CategoryHasProduct(category_has_product_obj.first())
        else:
            return None

    def update_position(self, category_id ,product_id, position):
       mall_models.CategoryHasProduct.update(display_index=position).dj_where(product_id=product_id, category_id=category_id).execute()

    @property
    def category(self):
        category_has_product_obj = self.context['db_model']
        return category_has_product_obj.category

    @property
    def product(self):
        category_has_product_obj = self.context['db_model']
        return category_has_product_obj.product


