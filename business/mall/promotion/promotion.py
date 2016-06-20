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


class Promotion(business_model.Model):
    """
    促销
    """
    __slots__ = (
        'id',
        'owner_id',
        'type',
        'display_type',
        'type_name',
        'name',
        'promotion_title',
        'status',
        'display_status',
        'start_date',
        'end_date',
        'member_grade_id',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['detail_id'])
    def from_detail_id(args):
        promotion_model = promotion_models.Promotion.get(detail_id=args['detail_id'])
        return Promotion(promotion_model)