# -*- coding: utf-8 -*-
"""@package business.mall.promotion.promotion
促销

"""
from datetime import datetime
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

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    @param_required(['detail_id'])
    def from_detail_id(args):
        promotion_model = promotion_models.Promotion.get(detail_id=args['detail_id'])
        return Promotion(promotion_model)

    def __get_real_status(self):
        """
		根据当前时间与start_date, end_date的关系，获取真实的status
		"""

        # TODO2: 处理promotion从数据库promotion_result加载的情况，后续将去掉这里的对self.start_date的判断逻辑
        if not self.start_date:
            return promotion_models.PROMOTION_STATUS_FINISHED

        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        if self.start_date > now:
            return promotion_models.PROMOTION_STATUS_NOT_START
        elif self.end_date < now:
            return promotion_models.PROMOTION_STATUS_FINISHED
        else:
            return promotion_models.PROMOTION_STATUS_STARTED

    def _init_promotion_slot_from_model(self, promotion_model):
        self._init_slot_from_model(promotion_model, Promotion.__slots__)
        self.start_date = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
        self.end_date = self.end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        self.status = self.status if self.status == promotion_models.PROMOTION_STATUS_FINISHED else self.__get_real_status()
        self.display_status = promotion_models.PROMOTIONSTATUS2NAME.get(self.status, u'未知')
        self.display_type = promotion_models.PROMOTION2TYPE.get(self.type, {'display_name': u'未知'})['display_name']
        self.type_name = promotion_models.PROMOTION2TYPE.get(self.type, {'name': u'unknown'})['name']

        self.context['detail_id'] = promotion_model.detail_id