# -*- coding: utf-8 -*-
"""@package business.mall.promotion.promotion
促销

"""
from datetime import datetime

from db.mall import promotion_models
from business import model as business_model


class Promotion(business_model.Model):
    """
    促销
    """
    __slots__ = (
        'id',
        'name',
        'promotion_title',
        'type',
        'type_name',
        'status',
        'start_date',
        'end_date',
        'member_grade_id',
        'detail',
        'products',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)
        self._init_slot_from_model(model)

        if model:
            self.start_date = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
            self.end_date = self.end_date.strftime("%Y-%m-%d %H:%M:%S")
            self.created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            self.status = self.status if self.status == promotion_models.PROMOTION_STATUS_FINISHED else self.__get_real_status()
            self.type_name = promotion_models.PROMOTION2TYPE.get(self.type, {'name': u'unknown'})['name']
            self.context['detail_id'] = model.detail_id

    def __get_real_status(self):
        """
        根据当前时间与start_date, end_date的关系，获取真实的status
        """
        # TODO2: 处理promotion从数据库promotion_result加载的情况，后续将去掉这里的对self.start_date的判断逻辑
        if not self.start_date:
            return promotion_models.PROMOTION_STATUS_FINISHED

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.start_date > now:
            return promotion_models.PROMOTION_STATUS_NOT_START
        elif self.end_date < now:
            return promotion_models.PROMOTION_STATUS_FINISHED
        else:
            return promotion_models.PROMOTION_STATUS_STARTED
