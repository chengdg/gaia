# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from business.mall.product import Product
from business.mall.category_factory import CategoryFactory


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
        category_factory_obj = CategoryFactory.post_category(args)
        category_obj = category_factory_obj.create()
        return Categories(category_obj)

    @property
    def __get_model(self):
        return self.context['db_model']

    @staticmethod
    @param_required(['category_id'])
    def get_for_category_by_id(args):
        '''
        获取单个分组信息
        '''
        obj = mall_models.ProductCategory.select().dj_where(id=args['category_id'])
        return Categories(obj.first())

    @staticmethod
    @param_required(['category_id'])
    def delete_for_category_by_id(args):
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

