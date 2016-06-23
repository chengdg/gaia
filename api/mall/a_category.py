# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.categories import Categories
from business.mall.category_factory import CategoryFactory

class Category(api_resource.ApiResource):
    app = 'mall'
    resource = 'category'

    @param_required(['name', 'owner_id'])
    def post(args):
        # print 'post++++++++++====category.....', args
        #由于在zeus测试平台，不能传列表，现由'1,2,3,4,5'这种方式处理
        product_ids = [product_id.strip() for product_id in args.get('product_ids', '').strip().split(',') if product_id]
        args.update(dict(product_ids=product_ids))
        '''
        创建商品分组,  利用工厂类@生成器
        '''
        category_factory_obj = CategoryFactory.create()
        category_obj = category_factory_obj.save(args['owner_id'], args['name'])
        return  {
            'category':category_obj.to_dict() 
        }

    @param_required(['category_id', 'name'])
    def put(args):
        # print 'put_=================category;;;;;;;;;;;', args
        opt = {
            'name': args['name']
        }
        category_obj = Categories.put_category({'category_id': args['category_id'], 'params': opt})
        return  {
            'category': category_obj.to_dict()
        }

    @param_required(['category_id'])
    def get(args):
        # print 'get_=================category;;;;;;;;;;;', args
        category_id = args['category_id']
        category_obj = Categories.from_id({'category_id': category_id})
        ret = {
            'category': category_obj.to_dict()
        }
        if args.get('is_has_product', None):
            ret['category'].update({
                    'products': [product.to_dict() for product in category_obj.products]
                })
        return ret

    @param_required(['category_id'])
    def delete(args):
        # print 'delete_=================category;;;;;;;;;;;', args
        action_count = Categories.delete_from_id(args)
        return {
            'influences': action_count
        }

