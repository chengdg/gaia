# -*- coding: utf-8 -*-
import logging

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

class CategoryFactory(business_model.Model):
    '''
    分组创建工厂@生成器
    '''
    __slots__=(
        )

    def __init__(self, owner, name, product_ids=[]):
        business_model.Model.__init__(self)
        self.context['owner'] = owner
        self.context['name'] = name
        self.context['product_count'] = len(product_ids)
        self.context['product_ids'] = product_ids

    @staticmethod
    @param_required(['owner', 'name'])
    def post_category(args):
        category_factory_obj = CategoryFactory(args['owner'], args['name'], args['product_ids'])
        return category_factory_obj


    def create_category_has_product(self):
        if self.is_has_products:
            opt = {
                'product_ids': self.context['product_ids'],
                'category_obj': self.context['db_model']
            }
            category_has_product_obj = CategoryHasProductFactory.post_category_has_product(opt)
            category_has_product_objs = category_has_product_obj.create_category_product_relation()
            self.context['category_has_product_relation'] = category_has_product_objs
            return category_has_product_obj.is_success

    def create(self):
        obj = None
        opt = dict(
            owner=self.context['owner'],
            name=self.context['name'],
            product_count=self.context['product_count']
        ) 
        # created is True or False  
        # If an object is found, get_or_create() returns a tuple of that object and False. 
        # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
        # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
        # try:
        obj, created = mall_models.ProductCategory.get_or_create(**opt)
        self.context['db_model'] = obj
        self.context['is_success'] = created

        if self.is_has_products:
            self.create_category_has_product()
        return obj

    @property
    def is_success(self):
        return self.context['is_success']

    @property
    def is_has_products(self):
        return  True if self.context['product_ids'] else False



class CategoryHasProductFactory(business_model.Model):
    '''
    创建分组中商品关系@生成器
    '''
    __slots__=(
        )

    def __init__(self, product_ids, category_obj):
        business_model.Model.__init__(self)
        self.context['product_ids'] = product_ids
        self.context['category_model'] = category_obj

    @staticmethod
    @param_required(['product_ids', 'category_obj'])
    def post_category_has_product(args):
        category_has_product_obj = CategoryHasProductFactory(args['product_ids'], args['category_obj'])
        return category_has_product_obj

    def create_category_product_relation(self):
        category_has_product = []
        is_relation_error = {}
        is_relation_success = []
        category_has_product_objs = []
        for product_id in self.context['product_ids']:
            opt =dict(
                product=mall_models.Product.get(id=product_id),
                category=self.context['category_model']
            )

           # created is True or False  
            # If an object is found, get_or_create() returns a tuple of that object and False. 
            # If multiple objects are found, get_or_create raises MultipleObjectsReturned. 
            # If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True
            try:
                obj, created = mall_models.CategoryHasProduct.get_or_create(**opt)
                category_has_product.append(obj)
                is_relation_success.append(product_id)
                category_has_product_objs.append(obj)
            except Exception, e:
                is_relation_error.update({product_id: str(e)})
        self.context['is_error'] = sorted(is_relation_error)
        self.context['is_success'] = sorted(is_relation_success)
        return category_has_product_objs if not is_relation_error else is_relation_error

    @property
    def is_error(self):
        return self.context['is_error']

    @property
    def is_success(self):
        '''
        返回0说明成功
        '''
        return True if cmp(self.context['is_success'], self.context['product_ids']) == 0 else False


