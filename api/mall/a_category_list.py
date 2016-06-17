# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ACategoryList(api_resource.ApiResource):
    """
    商品管理
    """
    app = 'mall'
    resource = 'category_list'

    @param_required(['category_ids'])
    def get(args):
        """
        商品管理---> 分组管理列表
        """
        category_ids = [category_id for category_id in args['category_ids'].split(',') if category_id]
        print '00077&&&&&&&&&&&&&&&.................',args, category_ids
        return {}