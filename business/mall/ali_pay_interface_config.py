# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class AliPayConfig(business_model.Model):
    """
    支付宝支付配置信息
    """

    __slots__ = (
        'id',
        'owner_id',
        'partner',
        'key',
        'private_key',
        'ali_public_key',
        'seller_email',
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
        model = mall_models.UserAlipayOrderConfig.select().dj_where(id=id).first()
        if model:
            return AliPayConfig(model)

    @staticmethod
    @param_required(['owner', 'pay_version', 'partner', 'key', 'private_key', 'ali_public_key', 'seller_email'])
    def create(args):
        config = mall_models.UserAlipayOrderConfig.create(**args)
        return AliPayConfig(config)

    def update(self, **kwargs):
        mall_models.UserAlipayOrderConfig.update(**kwargs).dj_where(id=self.id).execute()