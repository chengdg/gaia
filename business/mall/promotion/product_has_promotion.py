# -*- coding: utf-8 -*-
"""@package business.mall.promotion.promotion
促销

"""
import json

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
from db.mall import models as mall_models
from db.mall import promotion_models
from eaglet.core import watchdog
from business import model as business_model
import settings


class ProductHasPromotion(business_model.Model):
    """
    促销
    """
    __slots__ = (
        'id',
        'product_id',
        'promotion_id'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['promotion_id'])
    def from_promotion_id(args):
        models = promotion_models.ProductHasPromotion.select().dj_where(promotion_id=args['promotion_id'])
        relations = []
        for model in models:
            relations.append(ProductHasPromotion(model))
        return relations