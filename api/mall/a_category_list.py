# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.categories import Categories

class ACategoryList(api_resource.ApiResource):
    """
    商品管理
    """
    app = 'mall'
    resource = 'category_list'

    @param_required(['category_ids', 'owner'])
    def get(args):
        """
        商品管理---> 分组管理列表
        @param category_ids:分组id列表
        
        """
        category_ids = [category_id for category_id in args['category_ids'].split(',') if category_id]
        print '00077&&&&&&&&&&&&&&&.................',args, category_ids
        if 'all' in category_ids and len(category_ids) == 1:
            category_ids = list()
        elif 'all' in category_ids and len(category_ids) > 1:
            category_ids.remove('all')
        args.update({'category_ids': category_ids})
        categories = Categories.get_for_category(args)
        return categories