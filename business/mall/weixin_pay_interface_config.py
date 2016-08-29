# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class WeixinPayConfig(business_model.Model):
    """
    微信支付信息
    """

    __slots__ = (
        'id',
        'owner_id',
        'partner_id',
        'partner_key',
        'paysign_key',
        'pay_version'
    )

    def __init__(self, db_model=None):
        business_model.Model.__init__(self)

        self.context['db_model'] = db_model
        if db_model:
            self._init_slot_from_model(db_model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        id = args['id']
        model = mall_models.UserWeixinPayOrderConfig.select().dj_where(id=id).first()
        if model:
            return WeixinPayConfig(model)

    @staticmethod
    @param_required(['owner', 'pay_version', 'app_id', 'partner_id', 'partner_key', 'app_secret'])
    def create(args):
        config = mall_models.UserWeixinPayOrderConfig.create(**args)
        return WeixinPayConfig(config)

    def update(self, **kwargs):
        mall_models.UserWeixinPayOrderConfig.update(**kwargs).dj_where(id=self.id).execute()