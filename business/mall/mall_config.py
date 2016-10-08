# -*- coding: utf-8 -*-
import logging

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model

from db.mall import models as mall_models
from db.express import models as express_models
from db.account import models as account_models
from util import regional_util


class MallConfig(business_model.Model):
    """
    商城配置
    """

    __slots__ = (
        'show_product_sales',  # 通用设置，商品销量
        'show_product_sort',  # 通用设置，销量排行
        'show_product_search',  # 通用设置， 商品搜索框
        'show_shopping_cart',  # 通用设置， 购物车
        'created_at'  # 添加时间
    )

    def __init__(self, db_model):
        business_model.Model.__init__(self)
        self._init_slot_from_model(db_model)

    @staticmethod
    @param_required(['woid'])
    def get(args):
        woid = args['woid']
        db_model = MallConfig.__get_db_model(woid)

        return MallConfig(db_model)


    @staticmethod
    @param_required(['woid'])
    def set(args):
        woid = args['woid']
        db_model = MallConfig.__get_db_model(woid)
        db_model.show_product_sales = int(args.get('show_product_sales', '0'))
        db_model.show_product_sort = int(args.get('show_product_sort', '0'))
        db_model.show_product_search = int(args.get('show_product_search', '0'))
        db_model.show_shopping_cart = int(args.get('show_shopping_cart', '0'))
        db_model.save()
        # todo 清缓存
        return MallConfig(db_model)

    @staticmethod
    def __get_db_model(woid):
        user = account_models.User.get(id=woid)

        db_model, created = mall_models.MallConfig.get_or_create(
            owner=user,
            defaults={'order_expired_day': 24}
        )

        return db_model
