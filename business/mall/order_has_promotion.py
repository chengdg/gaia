# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from business import model as business_model

from db.mall import models as mall_models


class OrderHasPromotion(business_model.Model):
    """
    订单的促销
    """

    __slots__ = (
        'order_id', #订单的id
        'webapp_user_id',
        'promotion_id',
        'promotion_type',
        'promotion_result_json',
        'created_at',
        'integral_money',
        'integral_count'
    )

    def __init__(self):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        order_has_promotion = OrderHasPromotion(model)
        return order_has_promotion

    @staticmethod
    @param_required(['order_id'])
    def from_order(args):
        order_has_promotion_models = mall_models.OrderHasPromotion.select().dj_where(order_id=args['order_id'])
        order_has_promotion = []
        for model in order_has_promotion_models:
            order_has_promotion.append(OrderHasPromotion.from_model(model))
        return order_has_promotion

    @property
    def promotion_result(self):
        data = json.loads(self.promotion_result_json)
        data['type'] = self.promotion_type
        return data