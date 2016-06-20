# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_category import AProductCategory
from business.mall.categories import Categories

class Category(api_resource.ApiResource):
    app = 'mall'
    resource = 'category'

    @param_required(['name', 'owner'])
    def post(args):
        print 'post++++++++++====category.....', args
        #由于在zeus测试平台，不能传列表，现由'1,2,3,4,5'这种方式处理
        product_ids = [product_id.strip() for product_id in args.get('product_ids', '').strip().split(',') if product_id]
        args.update(dict(product_ids=product_ids))
        return  AProductCategory.post_for_category(args)

    @param_required(['category_id'])
    def put(args):
        print 'put_=================category;;;;;;;;;;;', args
        put_category_obj = Categories.put_category(args)
        return  put_category_obj
