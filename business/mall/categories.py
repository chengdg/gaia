# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from core import paginator
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
        'created_at'
    )
    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            model.product_count = 0
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['owner'])
    def  get_for_category(args):
        '''
        分组管理列表
        '''
        # print 'buession...................', args
        filter_params = dict(owner=args['owner'] )
        level = int(args['deep_level']) if 'deep_level' in args else 2
        # 分页
        page_info = dict(
            page=int(args['page']) if 'page' in args else 1,
             count_per_page=int(args['count_per_page']) if 'count_per_page' in args else 10
            )
        print page_info
        if args['category_ids']:
            filter_params.update({'id__in': args['category_ids']})
        categories = mall_models.ProductCategory.filter(**filter_params)
        return Categories.get_pageinfo_paginator(categories, is_paginator=not args['category_ids'], deep_level=level, **page_info)


    @staticmethod
    def get_pageinfo_paginator(category_models, is_paginator=False, deep_level=2, **kwargs):
        """
        分页管理
        """
        if is_paginator:
            cur_page = kwargs.get('page')
            count_per_page = kwargs.get('count_per_page')
            query_string = kwargs.get('query_string', None)
            pageinfo, categories = paginator.paginate(category_models, cur_page, count_per_page, query_string=query_string) 
            categories_objs = list()
            if deep_level == 2:
                for category in categories:
                    category_dict = category.to_dict()
                    category_dict.update(dict(products=Categories.get_category_product_relation(category)))
                    categories_objs.append(category_dict)
            else:
                categories_objs = [category.to_dict() for category in categories]
            return {
                'categories': categories_objs,
                'pageinfo': pageinfo.to_dict(),
            }
        else:
            categories_objs = list()
            if deep_level == 2:
                for category in category_models:
                    category_dict = category.to_dict()
                    category_dict.update(dict(products=Categories.get_category_product_relation(category)))
                    categories_objs.append(category_dict)
            else:
                categories_objs = [category.to_dict() for category in category_models]
            return {
                 'categories': categories_objs,
            }
    @staticmethod
    def get_category_product_relation(category_model):
        '''
        获取此分组中商品的内容
        '''
        relations = mall_models.CategoryHasProduct.filter(category=category_model)
        product_ids = [relation.product_id for relation in relations]
        return [product.to_dict() for  product in  Product.from_ids({'product_ids': product_ids})]

    @staticmethod
    @param_required(['category_id'])
    def put_category(args):
        '''
        修改分组原有属性，如：名称
        '''
        args.pop('wapi_id')
        args.pop('_method')
        kwargs = copy(args)
        kwargs.pop('category_id')
        mall_models.ProductCategory.update(**kwargs).dj_where(id=args['category_id']).execute()
        return  mall_models.ProductCategory.get(id=args['category_id']).to_dict()

    @staticmethod
    @param_required(['catagory_id', 'product_ids'])
    def put_category_product(args):
        '''
        修改分组内部商品
        '''
        return {}







