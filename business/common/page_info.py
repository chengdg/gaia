# -*- coding: utf-8 -*-

import settings
from eaglet.decorator import param_required
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.wxapi import get_weixin_api
from business import model as business_model

COUNT_PER_PAGE = 20

class PageInfo(business_model.Model):
    """
    微信service
    """
    __slots__ = (
        'cur_page',
        'count_per_page'
    )
    
    def __init__(self, cur_page, count_per_page):
        self.cur_page = cur_page
        self.count_per_page = count_per_page

    @staticmethod
    @param_required(['cur_page'])
    def create(args):
        return PageInfo(args['cur_page'], args.get('count_per_page', COUNT_PER_PAGE))